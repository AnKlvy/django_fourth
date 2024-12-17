import hashlib
import os

from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task, UploadedFile
from .forms import TaskForm, UploadedFileForm
from .services import check_user_exists, upload_file_to_minio, get_uploaded_files
from minio.error import S3Error

# Список всех задач (Read)
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

# Создание новой задачи (Create)
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user_pk = self.request.POST.get('user_pk')
        print(user_pk)
        if check_user_exists(user_pk):
            return super().form_valid(form)
        else:
            form.add_error(None, "Пользователь не найден.")
            return self.form_invalid(form)

# Обновление задачи (Update)
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user_pk = self.request.POST.get('user_pk')

        if check_user_exists(user_pk):
            return super().form_valid(form)
        else:
            form.add_error(None, "Пользователь не найден.")
            return self.form_invalid(form)

# Удаление задачи (Delete)
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    # def get(self, request, *args, **kwargs):
    #     user_pk = self.request.POST.get('user_pk')

        # if check_user_exists(user_pk):
        #     return super().get(request, *args, **kwargs)
        # else:
        #     return redirect('task-list')

# Загрузка файла (Create)
class UploadedFileCreateView(CreateView):
    model = UploadedFile
    form_class = UploadedFileForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('file_upload')

    def form_valid(self, form):
        file = form.cleaned_data.get('file')

        if file:
            original_name = file.name
            file_extension = os.path.splitext(original_name)[1]
            unique_name = hashlib.sha1(original_name.encode('utf-8')).hexdigest() + file_extension

            upload_file_to_minio(file, unique_name)

            form.instance = UploadedFile(
                original_name=original_name,
                unique_name=unique_name,
                file_extension=file_extension,
                file_size=file.size
            )
            return super().form_valid(form)
        else:
            form.add_error(None, "Ошибка при загрузке файла.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploaded_files = get_uploaded_files()

        for uploaded_file in uploaded_files:
            uploaded_file['object_name'] = UploadedFile.objects.get(unique_name=uploaded_file['object_name']).original_name

        context['updated_files'] = uploaded_files
        return context

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadedFileSerializer
from .services import upload_file_to_minio, get_uploaded_files

import hashlib
import os
from django.db import IntegrityError

class FileUploadAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        original_name = file.name
        file_extension = os.path.splitext(original_name)[1]
        unique_name = hashlib.sha1(original_name.encode('utf-8')).hexdigest() + file_extension

        # Проверка на существование файла с таким именем
        while UploadedFile.objects.filter(unique_name=unique_name).exists():
            unique_name = hashlib.sha1((unique_name + str(file.size)).encode('utf-8')).hexdigest() + file_extension

        try:
            upload_file_to_minio(file, unique_name)

            uploaded_file = UploadedFile.objects.create(
                original_name=original_name,
                unique_name=unique_name,
                file_extension=file_extension,
                file_size=file.size
            )

            serializer = UploadedFileSerializer(uploaded_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            print(f"Ошибка базы данных: {str(e)}")
            return Response({'error': 'Ошибка при сохранении данных в базу'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except S3Error as e:
            print(f"Ошибка MinIO: {str(e)}")
            return Response({'error': 'Ошибка загрузки файла в MinIO'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError as e:
            print(f"Ошибка валидации: {str(e)}")
            return Response({'error': 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Неизвестная ошибка: {str(e)}")
            return Response({'error': 'Неизвестная ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        files = get_uploaded_files()
        return Response(files, status=status.HTTP_200_OK)