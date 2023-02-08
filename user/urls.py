from django.urls import path, include
from user.api import views

url_patterns_user = [
    path('login/', views.login),
    path('set_password/<str:uid>/<str:token>/', views.forgot_password),
    path('create/', views.create),
    path('send_link_reset/', views.send_reset_link),

]
urlpatterns = [
    path('', include(url_patterns_user)),
]