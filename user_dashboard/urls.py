from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('saved-jobs/', views.saved_jobs_view, name='saved_jobs'),
    path('save-job/<slug:job_slug>/', views.save_job_view, name='save_job'),
    path('unsave-job/<slug:job_slug>/', views.unsave_job_view, name='unsave_job'),
]