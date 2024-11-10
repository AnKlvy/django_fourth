FROM python:bullseye

# Устанавливаем рабочую директорию
WORKDIR /usr/src/django_fourth

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем необходимые зависимости
RUN apt-get update \
    && apt-get install -y libpq-dev postgresql-client netcat-openbsd gcc python3-dev \
    && pip install --no-cache-dir -r requirements.txt



# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем проект
COPY . .

# Copy the wait-for script from local to container
COPY ./wait-for.sh /bin/wait-for.sh
RUN chmod 777 -R /bin/wait-for.sh
#RUN chmod +x entrypoint.sh  # Делаем скрипт исполняемым
#
## Укажите команду запуска
#ENTRYPOINT ["./entrypoint.sh"]
# Команда для запуска приложения
CMD sh -c "/bin/wait-for.sh db:5432 && /bin/wait-for.sh rabbitmq:5672 && \
           python manage.py runserver 0.0.0.0:8000"

