from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("get/", views.get_students, name='students'),
    path('register/', views.register_student, name='register'),
    path('edit/<str:ra>/', views.edit_student, name='edit'),
    path('delete/<str:ra>/', views.delete_student, name='delete'),
]