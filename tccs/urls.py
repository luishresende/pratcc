from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('tcc_work/register/', views.register_tcc_work, name='register_tcc_work'),
    path('tcc_work/edit/<int:tcc_id>/', views.edit_tcc_work, name='edit_tcc_work'),
    path('tcc_committe/register/', views.register_tcc_committe, name='register_tcc_committe'),
    path('tcc_committe/edit/<int:committe_id>/', views.edit_tcc_committe, name='edit_tcc_committe'),
    path('tcc_documents/register/<int:tcc_id>/', views.register_tcc_documents, name='register_tcc_documents'),
    path('tcc_documents/edit/<int:tcc_id>/', views.edit_tcc_documents, name='edit_tcc_documents'),
    path('get/', views.get_tcc_work, name='get_tcc_work'),
    path('delete/<int:tcc_id>/', views.delete_tcc_work, name='delete_tcc_work'),
]