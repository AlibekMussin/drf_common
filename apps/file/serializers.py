# Vendor
from rest_framework import serializers

# Local
from .models import File
from .utils import handle_uploaded_file
from apps.utils.exceptions import CustomException


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def save(self):
        file = self.validated_data['file']
        new_file_name = handle_uploaded_file(file)
        if not new_file_name:
            raise CustomException(translate_code="can_get_only_images",)
        print(f"new_file_name: {new_file_name}")
        new_file = File.objects.create(
            original_name=new_file_name,
            mime_type=file.content_type,
            file_path="uploads/" + new_file_name
        )
        return {
            'file_id': new_file.id,
            'original_name': new_file_name,
            'mime_type': file.content_type
        }

    class Meta:
        fields = "__all__"
        model = File

class FileGetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', "original_name", 'mime_type', 'hash_name' ]
        model = File
