from rest_framework import serializers
from apps.file_app import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileModel
        fields = "file_path", "title", "file_type", "user", "file_label"


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileTypeModel
        fields = "file_type", "file_type_remark"


class FileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileLabelModel
        fields = "file_label",


