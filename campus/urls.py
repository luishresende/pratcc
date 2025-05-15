from django.urls import path
from . import views


urlpatterns = [
    path('get-cities/', views.get_cities_by_state, name='get_cities_by_state'),
    path('register/', views.campus_register, name='campus_register'),
    path('edit/<int:id>/', views.edit_campus, name='campus_edit'),
    path('get/', views.get_campus, name='campus_list'),
    path('delete/<int:id>/', views.delete_campus, name='delete_campus'),
]