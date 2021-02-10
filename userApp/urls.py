from django.urls import path
from . import views

app_name = 'userApp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('request-meter/', views.meter_view, name='meter'),
    path('view-bill/', views.viewBill_view, name='viewBill'),
]