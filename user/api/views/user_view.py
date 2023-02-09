from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.utils.encoding import (
    force_text,
    force_bytes
)
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, \
    BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from base.token import account_activation_token
from user.models import User

from user.api.serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer
)


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer


create = CreateUser.as_view()


class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data.get('email').lower()
        if "@" in username:
            user = User.objects.filter(email=username)
            if user:
                user = user.first()
            else:
                return Response(
                    {"detail": "Пользователь не найден"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = User.objects.filter(phone=username)
            if user:
                user = user.first()
            else:
                return Response(
                    {"detail": "Пользователь не найден"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().post(request, *args, **kwargs)


login = Login.as_view()


class SendLinkResetPassword(APIView):

    def post(self, request, *args, **kwargs):
        host = "http://{}/api/user/".format(request.get_host())
        login = str(self.request.data.get('login')).lower()
        if "@" in login:
            user = User.objects.filter(email=login).first()
            try:
                mail_subject = 'Сброс пароля'
                message = render_to_string('send_reset_link.html', {
                    'user': user,
                    'domain': host,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    html_message=message
                )
            except:
                return Response({"error": "Сообщение не отправилось!"})
        else:
            user = User.objects.filter(phone=login).first()
            try:
                mail_subject = 'Сброс пароля'
                message = render_to_string('send_reset_link.html', {
                    'user': user,
                    'domain': request.get_host(),
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    html_message=message
                )
            except:
                return Response({"error": "Сообщение не отправилось!"})


        return Response({"send": "Отправлено"})


send_reset_link = SendLinkResetPassword.as_view()


class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uid')
        token = self.kwargs.get('token')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
            raise ValueError("Неправильные данные!")

        if user is not None:
            if account_activation_token.check_token(user, token):
                password = self.request.data.get('password')
                confirm_password = self.request.data.get('confirm_password')
                if (password == confirm_password):
                    user.set_password(password)
                    user.save()
                    return Response({"sucess": "Пароль успешно изменен!"})
            else:
                return Response({"error": "Токен не дейвствителен!"})
        else:
            return Response({"error": "Такой пользователь не сушевствует!"})


forgot_password = ForgotPasswordView.as_view()


