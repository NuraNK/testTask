from django.urls import path, include
from task.api import views

url_patterns_todo = [
    path('create/', views.create),
    path('detail/<int:id>/', views.detail),
    path('delete/<int:id>/', views.delete),
    path('list/', views.list),
    path('<int:id>/execute/', views.execute),

]
urlpatterns = [
    path('', include(url_patterns_todo)),
]