import os

from django import forms
from .models import Task, UploadedFile


class TaskForm(forms.ModelForm):
    user_pk = forms.IntegerField(widget=forms.NumberInput())  # Скрытое поле для user_pk

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_date', 'status', 'user_pk']  # Добавляем user_pk в список полей

class UploadedFileForm(forms.ModelForm):
    file = forms.FileField(label="Выберите файл")  # Поле для выбора файла

    class Meta:
        model = UploadedFile
        fields = []  # Указываем нужные поля

