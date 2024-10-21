from django_minio_backend import MinioBackend

minio_available = MinioBackend().is_minio_available()  # An empty string is fine this time
if minio_available:
    print("MINIO IS AVAILABLE")
else:
    print("MINIO ISN'T AVAILABLE!!!")
    print(minio_available.details)