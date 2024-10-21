#!/bin/sh

set -e  # Завершить скрипт при ошибке

# Вывод значений переменных
echo "DATABASE: $DATABASE"
echo "SQL_HOST: $SQL_HOST"
echo "SQL_PORT: $SQL_PORT"
echo "SQL_USER: $SQL_USER"
echo "SQL_PASSWORD: $SQL_PASSWORD"
echo "SQL_DATABASE: $SQL_DATABASE"

if [ "$DATABASE" = "postgres" ]; then
    echo "Ожидание подключения к PostgreSQL..."

    # Ждем, пока PostgreSQL станет доступен
    until pg_isready -h "$SQL_HOST" -p "$SQL_PORT" -U "$SQL_USER"; do
        echo "PostgreSQL недоступен, ждем..."
        sleep 2
    done

    echo "PostgreSQL запущен"

    # Проверяем, существует ли база данных
    if ! PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -p "$SQL_PORT" -U "$SQL_USER" -lqt | cut -d \| -f 1 | grep -qw "$SQL_DATABASE"; then
        echo "Создание базы данных $SQL_DATABASE..."
        PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -p "$SQL_PORT" -U "$SQL_USER" -c "CREATE DATABASE $SQL_DATABASE;"
    else
        echo "База данных $SQL_DATABASE уже существует."
    fi
fi

# Выполнение миграций
echo "Запуск миграций..."
PGPASSWORD="$SQL_PASSWORD" python manage.py migrate

exec "$@"
