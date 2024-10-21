import hashlib
import os

from django.db import models
from datetime import date
from storages.backends.s3boto3 import S3Boto3Storage

from django_fourth import settings


class Task(models.Model):
    STATUS_CHOICES = [
        (0, 'Created'),
        (1, 'In Progress'),
        (2, 'Done'),
        (3, 'Failed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline_date = models.DateField(default=date.today)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.title


# class PrivateAttachment(models.Model):
#     file = models.FileField(verbose_name="Object Upload",
#                             storage=MinioBackend(bucket_name='django-backend-dev-private'),
#                             upload_to=iso_date_prefix,
#                             )

class StaticS3Boto3Storage(S3Boto3Storage):
    location = settings.STATICFILES_STORAGE

    def __init__(self, *args, **kwargs):
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL
        super(StaticS3Boto3Storage, self).__init__(*args, **kwargs)


class S3MediaStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL
        super(S3MediaStorage, self).__init__(*args, **kwargs)

class UploadedFile(models.Model):
    original_name = models.CharField(max_length=255)  # Оригинальное имя файла
    unique_name = models.CharField(max_length=255, unique=True)  # Уникальное имя файла
    file_extension = models.CharField(max_length=10)  # Расширение файла
    file_size = models.PositiveIntegerField()  # Размер файла
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата загрузки

    def __str__(self):
        return self.original_name

    # def save(self, *args, **kwargs):
    #     if not self.unique_name:
    #         # Генерация уникального имени файла (например, sha1)
    #         hash_object = hashlib.sha1(self.original_name.encode('utf-8'))
    #         self.unique_name = hash_object.hexdigest() + os.path.splitext(self.original_name)[1]
    #     super().save(*args, **kwargs)


