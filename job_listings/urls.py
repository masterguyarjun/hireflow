from django.urls import path
from . import views

app_name = 'job_listings'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<slug:slug>/', views.job_detail_view, name='job_detail'),
    path('create/', views.job_create_view, name='job_create'),
    path('<slug:slug>/edit/', views.job_edit_view, name='job_edit'),
    path('<slug:slug>/delete/', views.job_delete_view, name='job_delete'),
    path('<slug:slug>/publish/', views.job_publish_view, name='job_publish'),
    path('<slug:slug>/close/', views.job_close_view, name='job_close'),
]