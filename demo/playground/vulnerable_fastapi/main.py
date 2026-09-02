"""
TorusGuard Playground: Vulnerable FastAPI Fixture
Contains 3 intentional security findings for demonstration purposes:
  - TG-INPUT-001 (SQL Injection)
  - TG-DB-004 (Missing Tenant Scoping)
  - TG-AGENT-001 (System Prompt Injection Concatenation)
"""

from typing import Optional, Dict, Any


class MockDB:
    def execute(self, query: str, params: Optional[tuple] = None):
        return [{"id": 1, "username": "admin", "data": "demo"}]

    def query(self, model: str):
        return self

    def filter(self, *conditions):
        return self

    def first(self):
        return {"id": 101, "tenant_id": "tenant_b", "amount": 5000}


db = MockDB()


# Finding 1: TG-INPUT-001 - Raw string interpolation into SQL query
def get_user_profile(user_id: str) -> Dict[str, Any]:
    query = f"SELECT id, username, email FROM users WHERE id = '{user_id}'"
    return db.execute(query)


# Finding 2: TG-DB-004 - Multi-tenant isolation failure (omits tenant filter)
def get_invoice_by_id(invoice_id: int) -> Dict[str, Any]:
    # VULNERABLE: Does not filter by request.user.tenant_id
    invoice = db.query("Invoice").filter(f"id == {invoice_id}").first()
    return invoice


# Finding 3: TG-AGENT-001 - Direct concatenation of user input into system prompt
def build_ai_chat_prompt(user_input: str) -> str:
    # VULNERABLE: Direct concatenation enables system instruction override
    system_prompt = f"You are a helpful customer support bot. Context: {user_input}\nHelp the customer."
    return system_prompt
