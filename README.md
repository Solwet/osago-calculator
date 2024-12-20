# Калькулятор стоимости ОСАГО
## Описание проекта
Этот проект представляет собой веб-сервис для расчёта стоимости обязательного страхования автогражданской ответственности (ОСАГО). Приложение позволяет пользователю ввести основные параметры водителя и автомобиля для динамического вычисления стоимости полиса.

## Функциональность
Валидация и обработка данных пользователя: даты рождения, стаж, мощность автомобиля, региональный коэффициент и история аварий.
Логика расчёта с учётом возраста, стажа водителя, мощности автомобиля, регионального коэффициента и количества аварий.
Интерактивный интерфейс с анимацией для удобного взаимодействия пользователя.
Отправка данных на сервер и вывод результата расчёта.
## Технологии и инструменты
### Backend
Python: Основной язык программирования.
FastAPI: Создание REST API для обработки запросов и выполнения расчётов.
Pydantic: Валидация входных данных пользователя.
CORS: Настройка для поддержки запросов с разных источников.
ngrok: Туннелирование для тестирования публичного доступа.
SSH: Развёртывание приложения на удалённом сервере.
Docker: Контейнеризация приложения (опционально).
### Frontend
HTML/CSS: Создание адаптивного и анимированного интерфейса.
JavaScript: Отправка данных на сервер и обработка ответа.
Анимации CSS: Плавные эффекты появления элементов и анимация машинки.

## Логика расчёта ОСАГО
### Расчёт стоимости выполняется с учётом:

Базовой ставки,
Возраст и стаж водителя,
Мощность автомобиля (л.с.),
Регионального коэффициента,
Коэффициента аварийности.
## Разработка:
### Back-end:
Мухтаров Руслан Айдынович
### Front-end: 
Пересыпкин Давид Валерьевич
### UI/UX дизайн:
Пестерев Андрей Евгеньевич
