from django.urls import path
from . import views


app_name = 'admin'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('editUser/', views.editUser_view, name="editUser"),
    path('editTariff/', views.editTariff_view, name="editTariff"),
    path('editFeeder/', views.editFeeder_view, name="editFeeder"),
    path('generateBill/', views.bill_view, name="bill"),
]