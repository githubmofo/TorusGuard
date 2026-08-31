from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Account

async def get_account_async(session: AsyncSession, account_id: int):
    # Unscoped modern select query
    stmt = select(Account).where(Account.id == account_id)
    result = await session.scalars(stmt)
    return result.first()
