"""
WOS n8n Executor v0
Executes n8n workflows via REST API
Bridges WOS Brain to n8n workflow execution
"""

import logging
import requests
import os
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("wos.n8n_executor")

class N8nExecutor:
    """
    n8n Workflow Executor v0
    
    Calls n8n workflows via REST API.
    Handles request/response transformation, error handling, timeouts.
    """
    
    def __init__(self, n8n_base_url: str = None, api_key: str = None):
        self.n8n_base_url = n8n_base_url or os.getenv("N8N_URL", "https://n8n.whyhi.app")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        
        if not self.api_key:
            logger.warning("N8N_API_KEY not set - n8n executor will fail")
    
    def execute_workflow(self, workflow_name: str, payload: Dict[str, Any],
                        timeout_seconds: int = 30) -> Dict[str, Any]:
        """
        Execute an n8n workflow via webhook
        
        Args:
            workflow_name: Name of the n8n workflow
            payload: Input data for the workflow
            timeout_seconds: Execution timeout
        
        Returns:
        {
            "status": "success" | "failed",
            "result": object,
            "error": str (if failed),
            "execution_time_ms": int,
            "workflow_name": str
        }
        """
        
        start_time = datetime.utcnow()
        
        try:
            # Build webhook URL
            webhook_url = f"{self.n8n_base_url}/webhook/{workflow_name}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"Executing n8n workflow: {workflow_name}")
            
            # Call n8n workflow
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=timeout_seconds
            )
            
            execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Handle response
            if response.status_code >= 400:
                logger.error(f"n8n workflow failed: {response.status_code} {response.text}")
                return {
                    "status": "failed",
                    "result": None,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "execution_time_ms": execution_time_ms,
                    "workflow_name": workflow_name
                }
            
            # Parse successful response
            try:
                result = response.json()
            except:
                result = response.text
            
            logger.info(f"n8n workflow succeeded: {workflow_name}")
            
            return {
                "status": "success",
                "result": result,
                "error": None,
                "execution_time_ms": execution_time_ms,
                "workflow_name": workflow_name,
                "status_code": response.status_code
            }
        
        except requests.Timeout:
            execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.error(f"n8n workflow timeout: {workflow_name}")
            return {
                "status": "failed",
                "result": None,
                "error": f"Workflow execution timeout ({timeout_seconds}s)",
                "execution_time_ms": execution_time_ms,
                "workflow_name": workflow_name
            }
        
        except Exception as e:
            execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.error(f"n8n executor error: {e}", exc_info=True)
            return {
                "status": "failed",
                "result": None,
                "error": str(e),
                "execution_time_ms": execution_time_ms,
                "workflow_name": workflow_name
            }
