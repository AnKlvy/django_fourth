# serializers.py
from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'original_name', 'unique_name', 'file_extension', 'file_size', 'uploaded_at']
