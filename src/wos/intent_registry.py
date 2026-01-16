"""
WOS Intent Registry v0
Manages intent definitions, routing, and policy in SQLite
Implements Phase 3.2 Brain Control Plane
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger("wos.intent_registry")

class IntentRegistry:
    """
    SQLite-backed intent registry following AOS Agent Registry spec.
    Stores intent definitions, approval policies, and n8n workflow mappings.
    """
    
    def __init__(self, db_path: str = "wos.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with intent registry schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Intent definitions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intents (
                intent_id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                version TEXT NOT NULL,
                description TEXT,
                handler_module TEXT NOT NULL,
                status TEXT DEFAULT 'draft',
                approval_required BOOLEAN DEFAULT 0,
                timeout_seconds INTEGER DEFAULT 30,
                max_retries INTEGER DEFAULT 2,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                owner TEXT DEFAULT 'wos'
            )
        """)
        
        # n8n workflow mappings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS n8n_workflows (
                workflow_id TEXT PRIMARY KEY,
                intent_id TEXT NOT NULL,
                n8n_workflow_name TEXT NOT NULL,
                n8n_webhook_url TEXT,
                input_schema TEXT,
                output_schema TEXT,
                active BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (intent_id) REFERENCES intents(intent_id)
            )
        """)
        
        # Intent execution log (audit trail)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intent_executions (
                execution_id TEXT PRIMARY KEY,
                request_id TEXT,
                intent_id TEXT NOT NULL,
                status TEXT,
                result JSON,
                error TEXT,
                execution_time_ms INTEGER,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (intent_id) REFERENCES intents(intent_id)
            )
        """)
        
        # Policy rules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS policy_rules (
                rule_id TEXT PRIMARY KEY,
                intent_id TEXT NOT NULL,
                rule_type TEXT,
                condition TEXT,
                action TEXT,
                enabled BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (intent_id) REFERENCES intents(intent_id)
            )
        """)
        
        self.conn.commit()
        logger.info(f"Intent registry initialized at {self.db_path}")
    
    def register_intent(self, intent_id: str, name: str, version: str, 
                       description: str, handler_module: str,
                       approval_required: bool = False,
                       timeout_seconds: int = 30) -> bool:
        """Register a new intent"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO intents (intent_id, name, version, description, 
                                    handler_module, approval_required, timeout_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (intent_id, name, version, description, handler_module, 
                  approval_required, timeout_seconds))
            self.conn.commit()
            logger.info(f"Registered intent: {name}")
            return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to register intent {name}: {e}")
            return False
    
    def map_workflow(self, workflow_id: str, intent_id: str, 
                    n8n_workflow_name: str, n8n_webhook_url: str = None,
                    input_schema: Dict = None, output_schema: Dict = None) -> bool:
        """Map an n8n workflow to an intent"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO n8n_workflows 
                (workflow_id, intent_id, n8n_workflow_name, n8n_webhook_url, 
                 input_schema, output_schema)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (workflow_id, intent_id, n8n_workflow_name, n8n_webhook_url,
                  json.dumps(input_schema) if input_schema else None,
                  json.dumps(output_schema) if output_schema else None))
            self.conn.commit()
            logger.info(f"Mapped workflow {n8n_workflow_name} to intent {intent_id}")
            return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to map workflow: {e}")
            return False
    
    def get_intent(self, intent_name: str) -> Optional[Dict]:
        """Look up intent by name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM intents WHERE name = ?", (intent_name,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_intent_by_id(self, intent_id: str) -> Optional[Dict]:
        """Look up intent by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM intents WHERE intent_id = ?", (intent_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_workflows_for_intent(self, intent_id: str) -> List[Dict]:
        """Get all n8n workflows mapped to an intent"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM n8n_workflows WHERE intent_id = ? AND active = 1", 
                      (intent_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def log_execution(self, execution_id: str, request_id: str, intent_id: str,
                     status: str, result: Dict = None, error: str = None,
                     execution_time_ms: int = None) -> bool:
        """Log an intent execution for audit trail"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO intent_executions 
                (execution_id, request_id, intent_id, status, result, error, execution_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (execution_id, request_id, intent_id, status,
                  json.dumps(result) if result else None, error, execution_time_ms))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to log execution: {e}")
            return False
    
    def requires_approval(self, intent_id: str) -> bool:
        """Check if intent requires approval"""
        intent = self.get_intent_by_id(intent_id)
        return intent.get("approval_required", False) if intent else False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()


# V0 Intent definitions (will be expanded)
INITIAL_INTENTS = [
    {
        "intent_id": "brief_generator_v0",
        "name": "brief_generator",
        "version": "0.1",
        "description": "Generate prospect/investor brief with Canon retrieval",
        "handler_module": "wos.intent_handlers.brief_generator",
        "approval_required": True,
        "timeout_seconds": 60
    },
    {
        "intent_id": "daily_email_digest_v0",
        "name": "daily_email_digest",
        "version": "0.1",
        "description": "Generate and send daily email digest",
        "handler_module": "wos.intent_handlers.daily_digest",
        "approval_required": False,
        "timeout_seconds": 30
    }
]
