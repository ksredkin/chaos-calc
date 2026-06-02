# 🧮 Chaos Calculator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-FCC21B?style=for-the-badge&logo=ruff&logoColor=black)

## 📄 Описание

**Chaos Calculator** — это необычный калькулятор, в котором правильность математического ответа определяется не законами логики, а мнением большинства. Это веб-приложение с асинхронным бэкендом на FastAPI и интерактивным фронтендом на React.

Здесь правильный ответ на выражение `2+2` — это тот результат, за который проголосовало больше всего пользователей. Полная математическая анархия, управляемая краудсорсингом!

## 📌 Скриншоты

*Frontend в процессе разработки*

## 📊 Статистика и качество

🧪 Покрытие кода тестами: **84%**

🛠 **Качество кода:** проект проходит строгую проверку **Ruff** (линтинг и форматирование) и **Mypy** (строгая статическая типизация).

🔄 **CI/CD:** настроен автоматический пайплайн в GitHub Actions (`main.yml`). При каждом пуше или пулл-реквесте автоматически запускаются тесты, проверяется линтер и контролируется уровень покрытия кода.

## 🧠 Компоненты системы

Архитектура приложения разделена на независимые слои:

* **API Layer (FastAPI):** Обрабатывает входящие HTTP-запросы, валидирует данные с помощью Pydantic-схем и управляет сессиями БД через Dependency Injection (`Depends`).
* **Repository Layer:** Инкапсулирует в себе всю сложную работу с базой данных (атомарные UPSERT-запросы на чистом SQLAlchemy).
* **Cache Service (Redis):** Обеспечивает мгновенную отдачу популярных и часто запрашиваемых выражений, снижая нагрузку на реляционную базу данных.
* **Database (PostgreSQL):** Надежное хранилище для двух связанных таблиц (`expressions` и `answers`) с каскадным удалением и уникальными индексами.

## 🎯 Возможности

* 🔍 **Расчет выражений:** получение текущего "лидирующего" ответа для любого математического примера.
* 🧑‍🏫 **Обучение калькулятора:** возможность проголосовать за свой вариант ответа (или предложить новый). Счетчик голосов обновляется атомарно.
* 📈 **Интерактивная статистика:** отображение топ-5 самых популярных ответов для конкретного выражения (идеально для графиков на фронтенде).
* ⚡ **Высокая скорость:** кэширование результатов вычислений в Redis.

## 📋 Требования

Для запуска проекта вам понадобятся:
* **Docker** и **Docker Compose** (рекомендуемый способ)

Для локальной разработки и запуска тестов (без Docker):
* **Python 3.14**
* **Poetry** (менеджер зависимостей)
* **Node.js** и **npm/bun** (для фронтенда)

## 🚀 Запуск проекта

1. Клонируйте репозиторий:
   ```Bash
   git clone https://github.com/ksredkin/chaos-calc.git
   cd chaos-calc
   ```

2. Создайте файл .env в корневом каталоге и настройте переменные окружения по примеру из .env.example.

3. Запустите всю инфраструктуру одной командой:
    ```Bash
    docker compose up --build -d
    ```

## ⭐ Примечание
Если проект показался вам интересным или забавным — не забудьте поставить ⭐ на GitHub! Это мотивирует развивать анархическую математику дальше. 🚀