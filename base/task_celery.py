
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.generics import get_object_or_404

from testTask import settings
from testTask.celery import app
from user.models import User


@app.task
def send_email(user):
    u = get_object_or_404(User, id=user)
    mail_subject = "Изменение статуса заданий"
    message = render_to_string('set_status.html', {
        'user': u
    })
    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [u.email],
        fail_silently=False,
        html_message=message,
    )