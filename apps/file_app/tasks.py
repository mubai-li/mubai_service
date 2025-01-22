from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from mubai_service.settings import FILE_SAVE_BASE_PATH

# 处理文件保存在本地的文件，目前没有想法，所以不写
@shared_task
def check_file(file_path):
    # file_dir_path = os.path.join(FILE_SAVE_BASE_PATH, str(user_id))
    # file_path = default_storage.save(os.path.join(file_dir_path, file_name), ContentFile(file_content))
    # return file_path
    pass
