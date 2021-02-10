from django.urls import path
from . import views


app_name = 'admin'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('edit-user/', views.editUser_view, name="editUser"),
    path('edit-tariff/', views.editTariff_view, name="editTariff"),
    path('edit-feeder/', views.editFeeder_view, name="editFeeder"),
    path('generate-bill/', views.bill_view, name="bill"),
]