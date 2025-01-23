from django.db.models.signals import post_save
from django.dispatch import receiver

from services.email import EmailService


@receiver(post_save)
def send_mail_confirm_user(sender, **kwargs):
    EmailService.send_mail(
        subject='Xác thực tài khoản',
        to_email=email
    )