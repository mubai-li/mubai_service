from django.db import models

from apps.user_app.models import UserModel


# Create your models here.

class FileModel(models.Model):
    id = models.AutoField(primary_key=True)
    file_path = models.FilePathField(verbose_name="文件路径")
    title = models.CharField(max_length=100, verbose_name="标题")
    file_type = models.ForeignKey(to="FileTypeModel", null=True, blank=False, on_delete=models.SET_NULL, verbose_name="文件类型")
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    file_label = models.ManyToManyField(
        to="FileLabelModel",
        through="File_FileLabelModel",
        through_fields=('files', 'file_labels')
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "apps_file_model"


class FileTypeModel(models.Model):
    id = models.AutoField(primary_key=True)
    file_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="文件类型")
    file_type_remark = models.TextField()

    def __str__(self):
        return self.file_type

    class Meta:
        db_table = "apps_file_type"


class FileLabelModel(models.Model):
    id = models.AutoField(primary_key=True)
    file_label = models.CharField(max_length=24, null=True, blank=True, verbose_name="文件标签")

    def __str__(self):
        return self.file_label

    class Meta:
        db_table = "apps_file_label"


class File_FileLabelModel(models.Model):
    id = models.AutoField(primary_key=True)
    files = models.ForeignKey(to="FileModel", on_delete=models.CASCADE)
    file_labels = models.ForeignKey(to="FileLabelModel", on_delete=models.CASCADE)

    def __str__(self):
        return self.files, self.file_labels

    class Meta:
        db_table = f"apps_file_file_label"
