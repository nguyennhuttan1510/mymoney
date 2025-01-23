from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class EmailService:
    @staticmethod
    def send_mail(subject: str, to_email: str, template_name: str, context: dict):
        try:
            email_body = render_to_string(template_name, context)

            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
            )
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }