from django.urls import path, include
from user.api import views

url_patterns_user = [
    path('login/', views.login),
    path('set_password/<str:uid>/<str:token>/', views.forgot_password),
    path('create/', views.create),
    path('send_link_reset/', views.send_reset_link),

    path('login_view/', views.login_view, name="login_view"),
    path('home_view/', views.home_view, name="home_view"),
    path('logout/', views.logout_view, name="logout_view"),

]
urlpatterns = [
    path('', include(url_patterns_user)),
]