from django.contrib import admin
from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, UploadedFileCreateView, \
    FileUploadAPIView
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TaskListView.as_view(), name='task-list'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),  # включение GraphiQL интерфейса
    path('upload/', UploadedFileCreateView.as_view(), name='file_upload'),  # Эндпоинт для загрузки файла
    path('api/files/', FileUploadAPIView.as_view(), name='file-upload-api'),
]
