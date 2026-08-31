from sqlalchemy.orm import Session
from .models import Account

def get_account_scoped(db: Session, account_id: int, tenant_id: str):
    return db.query(Account).filter(Account.id == account_id, Account.tenant_id == tenant_id).first()

def get_all_accounts_scoped(db: Session, tenant_id: str):
    return db.query(Account).filter(Account.tenant_id == tenant_id).all()
