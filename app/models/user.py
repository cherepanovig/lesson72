#from fastapi import APIRouter
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
#from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")


from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__))

# Создаем роутер с префиксом '/user' и тегом 'user'
router = APIRouter(prefix='/user', tags=['user'])


# Маршрут для получения всех пользователей
@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users'
        )
    return users


# Маршрут для получения пользователя по ID
@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    return user

# Маршрут для создания нового пользователя
@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)
    )
    db.execute(new_user)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


# Маршрут для обновления пользователя
@router.put('/update')
async def update_user(user: UpdateUser, user_id: int, db: Annotated[Session, Depends(get_db)]):
    upd_user = db.scalar(select(User).where(User.id == user_id))
    if upd_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(update(User).where(User.id == user_id).values(
        username=upd_user.username, # так как в схеме обновления пользователей нет username то подставляем username
        # найденного пользователя upd_user
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(upd_user.username)))

    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}



# Маршрут для удаления пользователя
@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    del_user = db.scalar(select(User).where(User.id == user_id))
    if del_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}

