"""
WOS Brain Control Plane v0 (UPDATED with Handler Integration)
Intent router implementing Phase 3.2 specification
Routes requests to intent handlers, enforces policy, returns Brain_Run_Response_v0
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from enum import Enum

logger = logging.getLogger("wos.brain")

class RequestStatus(str, Enum):
    """Brain request status values"""
    COMPLETED = "Completed"
    FAILED = "Failed"
    PAUSED = "Paused"
    PENDING_APPROVAL = "PendingApproval"

class Brain:
    """
    WOS Brain Control Plane
    
    Accepts normalized requests, enforces policy, routes to intent handlers,
    returns standardized Brain_Run_Response_v0
    
    Following AOS Constitution: Reliability First, Determinism Over Creativity, Operator Supremacy
    """
    
    def __init__(self, intent_registry, approval_gate, canon_tools, n8n_executor, 
                 handler_factory=None):
        """
        Initialize Brain with required components
        
        Args:
            intent_registry: IntentRegistry instance
            approval_gate: ApprovalGate instance
            canon_tools: Canon retrieval tools
            n8n_executor: n8n workflow executor
            handler_factory: Function to create handlers (from intent_handlers package)
        """
        self.intent_registry = intent_registry
        self.approval_gate = approval_gate
        self.canon_tools = canon_tools
        self.n8n_executor = n8n_executor
        self.handler_factory = handler_factory
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a Brain request following Phase 3.2 spec
        
        Input schema:
        {
            "request_id": string (required)
            "intent": string (required)
            "input": object (optional, default {})
            "mode": string (optional, e.g. "workflow_builder")
            "wb_stage": string (optional, "propose|test|approve|deploy")
        }
        
        Returns Brain_Run_Response_v0 envelope
        """
        
        # Step 1: Normalize request
        normalized = self._normalize_request(request)
        request_id = normalized["request_id"]
        
        try:
            # Step 2: Validate request
            if not self._validate_request(normalized):
                return self._error_response(
                    request_id, "INVALID_REQUEST", "Request validation failed"
                )
            
            # Step 3: Resolve intent
            resolved_intent = normalized["intent"].strip().lower()
            intent_record = self.intent_registry.get_intent(resolved_intent)
            
            if not intent_record:
                logger.warning(f"Intent not found: {resolved_intent}")
                return self._error_response(
                    request_id, "INTENT_NOT_FOUND", 
                    f"No intent registered for '{resolved_intent}'"
                )
            
            intent_id = intent_record["intent_id"]
            
            # Step 4: Policy guard - workflow_builder deploy requires approval
            if (normalized.get("mode") == "workflow_builder" and 
                normalized.get("wb_stage") == "deploy"):
                logger.info(f"WB deploy gate triggered for {request_id}")
                return self._paused_response(
                    request_id, intent_id, 
                    "Workflow builder deploy requires founder approval"
                )
            
            # Step 5: Check if intent requires approval
            if intent_record.get("approval_required"):
                approval_result = self.approval_gate.check_approval(
                    request_id, intent_id, normalized.get("input", {})
                )
                
                if not approval_result.get("approved"):
                    logger.info(f"Approval required for {intent_id}: {request_id}")
                    return self._pending_approval_response(
                        request_id, intent_id, approval_result
                    )
            
            # Step 6: Get and execute handler
            handler = self._get_handler(intent_record)
            if not handler:
                return self._error_response(
                    request_id, "HANDLER_NOT_FOUND",
                    f"Handler not available for {intent_id}"
                )
            
            execution_id = str(uuid.uuid4())
            
            # Validate input if handler supports it
            if hasattr(handler, 'validate_input'):
                if not handler.validate_input(normalized.get("input", {})):
                    return self._error_response(
                        request_id, "INVALID_INPUT",
                        "Input validation failed for intent"
                    )
            
            # Execute handler
            handler_result = handler.execute(
                request_id=request_id,
                execution_id=execution_id,
                intent_input=normalized.get("input", {}),
                intent_record=intent_record
            )
            
            # Step 7: Log execution
            self.intent_registry.log_execution(
                execution_id=execution_id,
                request_id=request_id,
                intent_id=intent_id,
                status=handler_result.get("status", "Unknown"),
                result=handler_result.get("result"),
                error=handler_result.get("error"),
                execution_time_ms=handler_result.get("execution_time_ms")
            )
            
            # Step 8: Return success or error response
            if handler_result.get("status") == "success":
                return self._success_response(
                    request_id, execution_id, intent_id, 
                    resolved_intent, handler_result
                )
            else:
                return self._error_response(
                    request_id, handler_result.get("error_code", "EXECUTION_FAILED"),
                    handler_result.get("error", "Intent execution failed")
                )
        
        except Exception as e:
            logger.error(f"Brain error processing {request_id}: {e}", exc_info=True)
            return self._error_response(
                request_id, "BRAIN_ERROR", str(e)
            )
    
    def _normalize_request(self, request: Dict) -> Dict:
        """Normalize request fields"""
        return {
            "request_id": request.get("request_id", str(uuid.uuid4())),
            "intent": request.get("intent", "").strip(),
            "input": request.get("input", {}),
            "mode": request.get("mode"),
            "wb_stage": request.get("wb_stage")
        }
    
    def _validate_request(self, request: Dict) -> bool:
        """Validate request has required fields"""
        required_fields = ["request_id", "intent"]
        return all(request.get(field) for field in required_fields)
    
    def _get_handler(self, intent_record: Dict):
        """
        Get handler for intent using factory
        """
        if not self.handler_factory:
            logger.error("Handler factory not configured")
            return None
        
        intent_id = intent_record["intent_id"]
        
        try:
            handler = self.handler_factory(
                intent_id=intent_id,
                n8n_executor=self.n8n_executor,
                approval_gate=self.approval_gate,
                canon_tools=self.canon_tools
            )
            return handler
        except Exception as e:
            logger.error(f"Failed to get handler for {intent_id}: {e}")
            return None
    
    # Response envelope generators
    
    def _success_response(self, request_id: str, execution_id: str, 
                         intent_id: str, resolved_intent: str,
                         handler_result: Dict) -> Dict:
        """Generate successful Brain_Run_Response_v0"""
        return {
            "ok": True,
            "status": RequestStatus.COMPLETED,
            "request_id": request_id,
            "execution_id": execution_id,
            "resolved_intent": resolved_intent,
            "intent_id": intent_id,
            "result": handler_result.get("result"),
            "timestamp": datetime.utcnow().isoformat(),
            "errors": []
        }
    
    def _error_response(self, request_id: str, error_code: str, 
                       error_message: str) -> Dict:
        """Generate error Brain_Run_Response_v0"""
        return {
            "ok": False,
            "status": RequestStatus.FAILED,
            "request_id": request_id,
            "execution_id": None,
            "resolved_intent": None,
            "result": None,
            "timestamp": datetime.utcnow().isoformat(),
            "errors": [{
                "code": error_code,
                "message": error_message,
                "stage": "brain"
            }]
        }
    
    def _paused_response(self, request_id: str, intent_id: str, 
                        reason: str) -> Dict:
        """Generate paused response (policy gate blocked)"""
        return {
            "ok": False,
            "status": RequestStatus.PAUSED,
            "request_id": request_id,
            "execution_id": None,
            "intent_id": intent_id,
            "result": None,
            "timestamp": datetime.utcnow().isoformat(),
            "approval": {
                "approval_required": True,
                "reason": reason
            },
            "errors": []
        }
    
    def _pending_approval_response(self, request_id: str, intent_id: str,
                                  approval_result: Dict) -> Dict:
        """Generate pending approval response"""
        return {
            "ok": False,
            "status": RequestStatus.PENDING_APPROVAL,
            "request_id": request_id,
            "execution_id": None,
            "intent_id": intent_id,
            "result": None,
            "timestamp": datetime.utcnow().isoformat(),
            "approval": approval_result,
            "errors": []
        }
