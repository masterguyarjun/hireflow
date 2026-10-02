from django.urls import path
from . import views

app_name = 'job_applications'

urlpatterns = [
    path('apply/<slug:job_slug>/', views.apply_for_job_view, name='apply_for_job'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('<int:application_id>/', views.application_detail_view, name='application_detail'),
    path('<int:application_id>/update-status/', views.update_application_status_view, name='update_application_status'),
]