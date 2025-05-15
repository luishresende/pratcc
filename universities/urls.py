from django.urls import path, include
from universities import views

urlpatterns = [
    path('register/', views.university_register, name='university_register'),
    path('get/', views.get_university_by_acronym, name='get_university_by_acronym'),
    path('edit/<str:acronym>/', views.edit_university, name='edit_university'),
    path('delete/<str:acronym>/', views.delete_university, name='delete_university'),
]
