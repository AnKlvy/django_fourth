# django_fourth/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Task, UploadedFile
from .forms import TaskForm, UploadedFileForm
from .services import *
import os
import hashlib

# Список всех задач (Read)
# @method_decorator(cache_page(60 * 3), name='dispatch')  # Кэшируем на 3 минут
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

# Обновление существующей задачи (Update)
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

# Удаление задачи (Delete)
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

# Загрузка файла (Create)
class UploadedFileCreateView(CreateView):
    model = UploadedFile
    form_class = UploadedFileForm
    template_name = 'files/upload.html'  # Убедитесь, что путь к шаблону верный
    success_url = reverse_lazy('file_upload')  # URL для перенаправления после успешной загрузки

    def form_valid(self, form):
        # Получаем файл из формы
        file = form.cleaned_data.get('file')

        if file:
            original_name = file.name
            file_size = file.size
            file_extension = os.path.splitext(original_name)[1]

            # Генерируем уникальное имя файла
            unique_name = hashlib.sha1(original_name.encode('utf-8')).hexdigest() + file_extension

            # Загружаем файл в MinIO
            upload_file_to_minio(file, unique_name)

            # Сохраняем данные о файле в базе данных
            uploaded_file = UploadedFile(
                original_name=original_name,
                unique_name=unique_name,
                file_extension=file_extension,
                file_size=file_size
            )
            uploaded_file.save()

            # Обновляем форму данными загруженного файла
            form.instance = uploaded_file

            return super().form_valid(form)
        else:
            form.add_error(None, "Ошибка при загрузке файла.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # Получаем контекст для отображения списка загруженных файлов
        context = super().get_context_data(**kwargs)
        # context['uploaded_files'] = get_uploaded_files()
        updated_files =[]
        uploaded_files = get_uploaded_files()
        for uploaded_file in uploaded_files:
            uploaded_file['object_name'] = UploadedFile.objects.get(unique_name=uploaded_file['object_name']).original_name
            # Добавляем измененный файл в новый список
            updated_files.append(uploaded_file)
        context['updated_files'] = updated_files

        print(context['updated_files'])
        return context