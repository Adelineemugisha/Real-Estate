from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from database import get_db
from app.repositories.user import UserRepository

bearer_scheme = HTTPBearer()

class UserService:
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: AsyncSession = Depends(get_db)):
        token = credentials.credentials
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise exception
        except jwt.PyJWTError:
            raise exception
            
        user = await UserRepository.get_by_email(db, email)
        if user is None:
            raise exception
        return user

    @staticmethod
    async def require_buyer_or_agent(current_user = Depends(get_current_user)):
        if current_user.role not in ("buyer", "agent"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted to buyers and agents only"
            )
        return current_user
