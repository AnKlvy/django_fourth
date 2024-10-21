import timeit
from django.test import Client
from django.core.cache import cache

# Создаем тестовый клиент
client = Client()

# URL для представления списка задач
url =  '/'

# Функция для очистки кэша и выполнения запроса без кэша
def fetch_without_cache():
    cache.clear()  # Очищаем кэш перед запросом
    response = client.get(url)
    return response.status_code

# Функция для выполнения запроса с кэшем
def fetch_with_cache():
    response = client.get(url)
    return response.status_code

# Замер времени для запросов без кэша
print("Время выполнения без кэша:")
time_without_cache = timeit.timeit('fetch_without_cache()', globals=globals(), number=10)
print(f"Среднее время без кэша: {time_without_cache / 10:.4f} секунд")

# Замер времени для запросов с кэшем
print("Время выполнения с кэшем:")
time_with_cache = timeit.timeit('fetch_with_cache()', globals=globals(), number=10)
print(f"Среднее время с кэшем: {time_with_cache / 10:.4f} секунд")
