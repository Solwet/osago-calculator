from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
<<<<<<< HEAD
=======
from datetime import datetime
from pyngrok import ngrok  # Подключаем pyngrok
from fastapi.logger import logger
import logging
>>>>>>> 52db5d396c464f8667d7e7958ebd78662948fc05


app = FastAPI()


# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно временно разрешить запросы со всех доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)
logger.debug("CORS middleware настроено правильно")
# Подключаем папку frontend как источник статических файлов
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Маршрут для главной страницы, возвращающий index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


# Определение коэффициентов для расчета ОСАГО
BASE_RATE = 5005  # Базовая ставка в рублях

class InsuranceData(BaseModel):
    age: int  # Возраст водителя
    experience: int  # Водительский стаж в годах
    power: int  # Мощность автомобиля в л.с.
    region_factor: float  # Региональный коэффициент
    accident_history: int  # Количество аварий за последние годы


def calculate_osago(data: InsuranceData) -> float:
    """
    Логика расчёта стоимости ОСАГО.
    """
    # Проверка вводных данных
    if data.age < 18:
        raise ValueError("Возраст должен быть 18 лет или больше.")
    if data.experience < 0:
        raise ValueError("Стаж не может быть отрицательным.")
    if data.power <= 0:
        raise ValueError("Мощность автомобиля должна быть больше 0.")

    # Коэффициент мощности
    if data.power <= 50:
        power_factor = 0.6
    elif data.power <= 100:
        power_factor = 1.0
    elif data.power <= 150:
        power_factor = 1.4
    else:
        power_factor = 1.6

    # Коэффициент возраста и стажа
    if data.age < 22 and data.experience < 3:
        age_experience_factor = 1.8
    elif data.age < 22:
        age_experience_factor = 1.6
    elif data.experience < 3:
        age_experience_factor = 1.7
    else:
        age_experience_factor = 1.0

    # Коэффициент аварийности
    accident_factor = 1 + (0.25 * data.accident_history)

    # Итоговая стоимость ОСАГО
    total_cost = (
        BASE_RATE * power_factor * age_experience_factor * data.region_factor * accident_factor
    )
    return round(total_cost, 2)


@app.post("/calculate")
def calculate_insurance(data: InsuranceData):
    """
    Эндпоинт для расчета стоимости ОСАГО.
    """
    try:
        result = calculate_osago(data)
        return {"osago_cost": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
<<<<<<< HEAD

=======
    


# Запуск ngrok при старте приложения
@app.on_event("startup")
async def startup_event():
    # Открываем ngrok туннель на 8000 порту
    public_url = ngrok.connect(8000)
    print(f"ngrok tunnel opened at {public_url}")


# Запуск ngrok при завершении приложения
@app.on_event("shutdown")
async def shutdown_event():
    ngrok.disconnect_all()
>>>>>>> 52db5d396c464f8667d7e7958ebd78662948fc05
