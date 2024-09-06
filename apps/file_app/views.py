from apps.file_app import models
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework import permissions
from utils.apiresponse import ResponseCode, APIResponse
from rest_framework import request
from django.http import StreamingHttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from mubai_service import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.file_app import file_app_serializers
import os


# Create your views here.
# views.py


def success(request):
    return render(request, 'success.html')


class UpAndDownFileGAPIView(generics.GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = file_app_serializers.FileSerializer

    def get(self, request: request.Request):
        task_file_id = request.query_params.get("task_file_id", None)
        if task_file_id is None:
            return APIResponse(code=ResponseCode.ERROR, msg="没有这个任务")

        task_file_obj = self.get_queryset().filter(id=task_file_id).first()
        if task_file_obj:
            file_path = os.path.join(settings.STATIC_URL, task_file_obj.file_path)
            if not os.path.exists(file_path):
                return APIResponse(code=ResponseCode.ERROR, msg="没有这个文件")

            file = open(file_path, 'rb')
            file_size = os.path.getsize(file_path)
            response = StreamingHttpResponse(FileWrapper(file, 8192),
                                             content_type='application/octet-stream')
            response['Content-Length'] = file_size
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(task_file_obj.file_name)
            return response

        return APIResponse(code=ResponseCode.ERROR, msg='文件没有发现')

    def post(self, request: request.Request):
        # user: models.UserModel = request.user

        file_dir_path = os.path.join(settings.FILE_SAVE_BASE_PATH, request.user.id)
        for file_name, file_obj in request.FILES.items():
            # print(file_obj)
            # print(file_name, file_obj.name)

            file_name = default_storage.save(os.path.join(file_dir_path, file_name), ContentFile(file_obj.read()))

        # print(file_name)
        #     file_path = default_storage.path(file_name)
        # print(file_path)
        # # 保存文件信息到数据库
        # task_file_obj = models.TaskFile(
        #     file_name=file_obj.name,
        #     file_path=file_path
        # )
        # task_file_obj.save()
        # file_model_obj = models.FileModel(
        #     title=file_name,
        #     file_path=file_path,
        #     user=user
        # )
        # file_model_obj.save()
        return APIResponse(code=ResponseCode.SUCCESS, msg="文件上传成功", data={"file_id": 1})


class FileTypeView(generics.GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = file_app_serializers.FileTypeSerializer

    def post(self, request: request.Request):
        file_type_ser: file_app_serializers.FileTypeSerializer = self.get_serializer(data=request.data)
        if file_type_ser.is_valid():
            file_type_ser.save()
            return APIResponse(code=ResponseCode.SUCCESS, msg="文件类型添加成功")
        return APIResponse(code=ResponseCode.ERROR, msg=file_type_ser.errors)


class FileLabelView(generics.GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = file_app_serializers.FileLabelSerializer

    def post(self, request: request.Request):
        file_label_ser: file_app_serializers.FileTypeSerializer = self.get_serializer(data=request.data)
        if file_label_ser.is_valid():
            return APIResponse(code=ResponseCode.SUCCESS, msg="文件标签添加成功")
        return APIResponse(code=ResponseCode.ERROR, msg=file_label_ser.errors)
