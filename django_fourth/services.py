import requests
from minio import Minio
from minio.error import S3Error
from django.conf import settings


def upload_file_to_minio(file, unique_name):
    # Используем правильный endpoint для локального MinIO
    client = Minio(
        settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=False  # Если MinIO не использует HTTPS
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # Проверка существования ведра
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Создано ведро", bucket_name)
    else:
        print("Ведро", bucket_name, "уже существует")

    try:
        # Загрузка файла в MinIO
        client.put_object(
            bucket_name, unique_name, file, length=-1, part_size=10*1024*1024,
        )
        print(f"Файл {unique_name} успешно загружен в ведро {bucket_name}")
    except S3Error as exc:
        print("Произошла ошибка:", exc)

def get_uploaded_files():
    client = Minio(
        settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=False  # Если MinIO не использует HTTPS
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    try:
        # Получаем список объектов из ведра
        objects = client.list_objects(bucket_name)
        file_list = []
        for obj in objects:
            presigned_url = client.presigned_get_object(bucket_name, obj.object_name)
            file_list.append({
                'object_name': obj.object_name,
                'presigned_url': presigned_url
            })
        return file_list
    except S3Error as exc:
        print("Произошла ошибка:", exc)
        return []

    # Проверка существования пользователя по user_pk
def check_user_exists(user_pk):
    headers = {
        'Host': 'localhost:8001'
    }
    response = requests.get(f'http://user_service:8001/api/user/{user_pk}/', headers=headers)
    print("User response status: ")
    print(response.status_code)
    return response.status_code == 200