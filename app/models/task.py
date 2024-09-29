from app.models.user import User  # Импортируем только класс User
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from fastapi import APIRouter





class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))



# Создаем роутер с префиксом '/task' и тегом 'task'
router = APIRouter(prefix='/task', tags=['task'])


# Маршрут для получения всех задач
@router.get('/')
async def all_tasks():
    pass


# Маршрут для получения задачи по ID
@router.get('/{task_id}')
async def task_by_id(task_id: int):
    pass


# Маршрут для создания новой задачи
@router.post('/create')
async def create_task():
    pass


# Маршрут для обновления задачи
@router.put('/update')
async def update_task():
    pass


# Маршрут для удаления задачи
@router.delete('/delete')
async def delete_task():
    pass

