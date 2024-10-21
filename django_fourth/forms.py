import os

from django import forms
from .models import Task, UploadedFile


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_date', 'status']

class UploadedFileForm(forms.ModelForm):
    file = forms.FileField(label="Выберите файл")  # Поле для выбора файла

    class Meta:
        model = UploadedFile
        fields = []  # Указываем нужные поля

    # def save(self, *args, **kwargs):
    #     # Здесь вы можете дополнительно обработать загружаемый файл, например, сохранить его на сервере.
    #     uploaded_file = self.cleaned_data.get('file')  # Доступ к загруженному файлу
    #     self.instance.original_name = uploaded_file.name
    #     self.instance.file_extension = os.path.splitext(uploaded_file.name)[1].lstrip('.')
    #     self.instance.file_size = uploaded_file.size
    #     super().save(*args, **kwargs)
