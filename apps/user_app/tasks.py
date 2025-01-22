import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
from celery import shared_task
from mubai_service import settings

from django.core.mail import send_mail

# 生成随机验证码
def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


# 发送验证码邮件
# def send_verification_email(receiver_email, code):
#     # 邮件配置
#     smtp_server = 'smtp.qq.com'  # QQ 邮箱的 SMTP 服务器
#     smtp_port = 465  # SSL 端口
#     sender_email = 'your_email@qq.com'  # 发件人邮箱
#     sender_password = 'your_authorization_code'  # 发件人邮箱授权码
#
#     # 邮件内容
#     subject = '您的验证码'
#     content = f'您的验证码是：{code}，请在 5 分钟内使用。'
#     message = MIMEText(content, 'plain', 'utf-8')
#     message['From'] = Header(sender_email, 'utf-8')
#     message['To'] = Header(receiver_email, 'utf-8')
#     message['Subject'] = Header(subject, 'utf-8')
#
#     try:
#         # 连接 SMTP 服务器
#         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#             server.login(sender_email, sender_password)  # 登录邮箱
#             server.sendmail(sender_email, receiver_email, message.as_string())  # 发送邮件
#         print('验证码邮件发送成功！')
#     except Exception as e:
#         print(f'邮件发送失败：{e}')
@shared_task
def send_verification_email_async(receiver_email, code):
    subject = '您的验证码'
    message = f'您的验证码是：{code}，请在 5 分钟内使用。'
    sender_email = settings.DEFAULT_FROM_EMAIL  # 从 settings.py 中获取发件人邮箱

    try:
        send_mail(
            subject,
            message,
            sender_email,
            [receiver_email],
            fail_silently=False,
        )
        return f'邮件发送成功：{receiver_email}'
    except Exception as e:
        return f'邮件发送失败：{e}'

# 示例：发送验证码
if __name__ == '__main__':
    pass
    # receiver_email = 'receiver@example.com'  # 收件人邮箱
    # verification_code = generate_verification_code()  # 生成验证码
    # send_verification_email(receiver_email, verification_code)  # 发送邮件
