from sqlalchemy.orm import Session
from .models import Account

def get_account_unscoped(db: Session, account_id: int):
    # Unscoped tenant query
    return db.query(Account).filter(Account.id == account_id).first()

def get_all_accounts(db: Session):
    # Global unscoped query
    return db.query(Account).all()
