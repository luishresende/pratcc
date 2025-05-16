from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('report/', views.report, name='report'),
    path('status/', views.tccs_status_geral, name='info'),
]