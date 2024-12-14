from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI()

# Определение коэффициентов для расчета ОСАГО
BASE_RATE = 5000  # Базовая ставка в рублях

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


@app.get("/")
def read_root():
    return {"Сообщение": "Калькулятор ОСАГО к вашим услугам!"}
