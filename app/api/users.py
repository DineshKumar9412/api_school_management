# api/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Query
from database.session import get_db
from models.user import User
from schemas.user import UserRead, UserCreate
from response.result import Result

router = APIRouter()

@router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.post("/new_row_user/", response_model=UserRead)
async def post_users_value(item: UserCreate,db: AsyncSession = Depends(get_db)):
    user = User(name=item.name,email=item.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/get_value_user/", response_model=UserRead)
async def get_value(name: str = Query(...),email: str = Query(...),db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.name == name,User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return {"message": "User not found"}
    return user