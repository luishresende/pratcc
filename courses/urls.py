from django.urls import path
from courses import views

urlpatterns = [
    path("", views.index, name='index'),
    path('register/', views.course_register, name='course_register'),
    path('get/', views.get_courses, name='courses_list'),
    path('edit/<int:id>/', views.edit_course, name='edit_course'),
    path('delete/<int:id>/', views.delete_course, name='delete_course'),
]