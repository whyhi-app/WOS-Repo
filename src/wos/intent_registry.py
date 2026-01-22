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
                execution_mode TEXT DEFAULT 'wos_managed',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                owner TEXT DEFAULT 'wos'
            )
        """)

        # Add new columns if they don't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE intents ADD COLUMN execution_mode TEXT DEFAULT 'wos_managed'")
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            cursor.execute("ALTER TABLE intents ADD COLUMN notes TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
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
                       timeout_seconds: int = 30,
                       execution_mode: str = 'wos_managed',
                       notes: str = None) -> bool:
        """
        Register a new intent

        Args:
            intent_id: Unique intent identifier
            name: Intent name
            version: Intent version
            description: Intent description
            handler_module: Python module path for handler
            approval_required: Whether approval is required before execution
            timeout_seconds: Execution timeout in seconds
            execution_mode: Execution mode - one of:
                - 'wos_managed': WOS Brain triggers (default)
                - 'autonomous_cron': n8n Cron trigger
                - 'autonomous_webhook': n8n email/webhook trigger
                - 'manual': User triggers in n8n UI
            notes: Optional notes about the intent
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO intents (intent_id, name, version, description,
                                    handler_module, approval_required, timeout_seconds,
                                    execution_mode, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (intent_id, name, version, description, handler_module,
                  approval_required, timeout_seconds, execution_mode, notes))
            self.conn.commit()
            logger.info(f"Registered intent: {name} (mode: {execution_mode})")
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

    def list_intents(self) -> List[Dict]:
        """List all registered intents"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM intents ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def list_intents_by_mode(self, execution_mode: str) -> List[Dict]:
        """
        List all intents with a specific execution mode

        Args:
            execution_mode: Execution mode to filter by
                - 'wos_managed': WOS Brain triggers
                - 'autonomous_cron': n8n Cron trigger
                - 'autonomous_webhook': n8n email/webhook trigger
                - 'manual': User triggers in n8n UI

        Returns:
            List of intent dictionaries matching the execution mode
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM intents WHERE execution_mode = ? ORDER BY created_at DESC",
            (execution_mode,)
        )
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
        "timeout_seconds": 60,
        "execution_mode": "wos_managed",
        "notes": None
    },
    {
        "intent_id": "daily_newsletter_digest_v0",
        "name": "daily_newsletter_digest",
        "version": "0.1",
        "description": "Generate and send daily newsletter digest",
        "handler_module": "wos.intent_handlers.daily_newsletter_digest",
        "approval_required": False,
        "timeout_seconds": 30,
        "execution_mode": "wos_managed",
        "notes": "WOS-managed daily newsletter digest. Triggered by Brain on schedule."
    },
    {
        "intent_id": "gmail_to_notion_task_v0",
        "name": "gmail_to_notion_task",
        "version": "0.1",
        "description": "Auto-create Notion task from forwarded email",
        "handler_module": "none",
        "approval_required": False,
        "timeout_seconds": 30,
        "execution_mode": "autonomous_webhook",
        "notes": "Triggered by email arrival in Gmail. Creates task in Notion tasks-masterlist database."
    },
    {
        "intent_id": "apple_reminders_to_notion_sync_v0",
        "name": "apple_reminders_to_notion_sync",
        "version": "0.1",
        "description": "Sync Apple Reminders to Notion twice daily",
        "handler_module": "none",
        "approval_required": False,
        "timeout_seconds": 60,
        "execution_mode": "autonomous_webhook",
        "notes": "Triggered by iOS Shortcuts automation (twice daily). Fetches Apple Reminders from 'Notion' list (last 12h), creates tasks in Notion tasks-masterlist."
    },
    {
        "intent_id": "creator_capture_v0",
        "name": "creator_capture",
        "version": "0.1",
        "description": "Capture creator links and populate CRM with contact info",
        "handler_module": "none",
        "approval_required": False,
        "timeout_seconds": 30,
        "execution_mode": "autonomous_webhook",
        "notes": "Triggered by webhook (iOS Shortcut share sheet). Extracts creator info from URL (Twitter, Instagram, YouTube, TikTok, LinkedIn, articles), determines contact method (DM vs email), stores in Notion CRM with 'New Lead' status."
    },
    {
        "intent_id": "creator_outreach_v0",
        "name": "creator_outreach",
        "version": "0.1",
        "description": "Generate personalized creator outreach with HITL approval",
        "handler_module": "wos.intent_handlers.creator_outreach",
        "approval_required": True,
        "timeout_seconds": 600,
        "execution_mode": "wos_managed",
        "notes": "WOS-managed outreach to creators/journalists. Queries CRM by status, generates personalized messages referencing original content, routes through Approval Gate, updates CRM status on approval."
    },
    {
        "intent_id": "content_idea_miner_v1",
        "name": "content_idea_miner",
        "version": "1.0",
        "description": "Analyze captured content and generate 2-5 content ideas using Canon",
        "handler_module": "wos.intent_handlers.content_idea_miner",
        "approval_required": False,
        "timeout_seconds": 120,
        "execution_mode": "wos_managed",
        "notes": "COS Phase 2 - Queries Content & Creator Capture for 'Sent to COS' status, loads Brand Foundation + Content Playbook, generates 2-5 ideas using Claude, creates entries in Content Ideas Queue, updates status to 'Ideas Generated'."
    }
]
