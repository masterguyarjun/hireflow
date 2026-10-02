from django.urls import path
from . import views

app_name = 'company_profiles'

urlpatterns = [
    path('', views.company_list_view, name='company_list'),
    path('<int:company_id>/', views.company_detail_view, name='company_detail'),
]