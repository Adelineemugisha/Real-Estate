from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserLogin
from app.schemas.token import Token
from app.repositories.user import UserRepository
from app.services.security import SecurityService
from app.services.user import UserService

router = APIRouter(prefix="/api/user", tags=["Users & Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await UserRepository.get_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await UserRepository.create(db, user_in)

@router.post("/login", response_model=Token)
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await UserRepository.get_by_email(db, login_in.email)
    if not user or not SecurityService.verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = SecurityService.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_current_user_profile(current_user = Depends(UserService.get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    return await UserRepository.get_all(db)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to update this user")
    updated_user = await UserRepository.update(db, user_id, user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this user")
    success = await UserRepository.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None