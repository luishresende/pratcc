from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("get/", views.get_teachers, name='teachers'),
    path("register/", views.register_teacher, name='add_teacher'),
    path('edit/<str:ma>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<str:ma>/', views.delete_teacher, name='delete_teacher'),
]