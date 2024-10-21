FROM python:bullseye

# Устанавливаем рабочую директорию
WORKDIR /usr/src/django_fourth

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем необходимые зависимости
RUN apt-get update \
    && apt-get install -y libpq-dev postgresql-client gcc python3-dev \
    && pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем проект
COPY . .

RUN chmod +x entrypoint.sh  # Делаем скрипт исполняемым

# Укажите команду запуска
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

