from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core import security
from app.schemas.token import Token

class AuthService:
    @staticmethod
    async def authenticate(
        db: AsyncSession, 
        username_or_email: str, 
        password: str
    ) -> Optional[User]:

        query = select(User).where(
            (User.username == username_or_email) | (User.email == username_or_email)
        )
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            return None
        
        if not security.verify_password(password, user.password_hash):
            return None
            
        return user

    @staticmethod
    def create_token_for_user(user: User) -> Token:

        access_token = security.create_access_token(
            subject=user.id,
            role=user.role.value
        )
        return Token(
            access_token=access_token, 
            token_type="bearer"
        )