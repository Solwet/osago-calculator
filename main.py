from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешает любые заголовки
)

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
    birth_date: str  # Дата рождения
    license_date: str  # Дата получения прав
    power: int  # Мощность автомобиля в л.с.
    region_factor: float  # Региональный коэффициент
    accident_history: int  # Количество аварий за последние годы

def calculate_osago(data: InsuranceData) -> float:
    """
    Логика расчёта стоимости ОСАГО.
    """
    # Рассчитываем возраст и стаж
    current_date = datetime.now()
    birth_date = datetime.strptime(data.birth_date, "%Y-%m-%d")
    license_date = datetime.strptime(data.license_date, "%Y-%m-%d")
    age = (current_date - birth_date).days // 365
    experience = (current_date - license_date).days // 365

    # Проверка вводных данных
    if age < 18:
        raise ValueError("Возраст должен быть 18 лет или больше.")
    if experience < 0:
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
    if age < 22 and experience < 3:
        age_experience_factor = 1.8
    elif age < 22:
        age_experience_factor = 1.6
    elif experience < 3:
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
