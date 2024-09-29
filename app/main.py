from fastapi import FastAPI
from app.models.task import router as task_router  # Импортируем роутер из task.py
from app.models.user import router as user_router  # Импортируем роутер из user.py

# Создаем экземпляр приложения FastAPI
app = FastAPI()


# Маршрут для корневого пути '/'
@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}


# Подключаем маршруты из task.py
app.include_router(task_router)

# Подключаем маршруты из user.py
app.include_router(user_router)
