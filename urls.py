from django.contrib import admin
from django.urls import path, include
from spis_tel import views
from spis_tel import models

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='list'),
    path('add_osoba',views.CreateOsoba.as_view(), name='add_osoba'),
    path('add_telefon/<pk>',views.CreateTelefon.as_view(), name='add_telefon'),
    path('add_email/<pk>',views.CreateEmail.as_view(), name='add_email'),
    path('update/<pk>', views.UpdateOsoba.as_view(), name='update'),
    path('delete/<pk>', views.DeleteOsoba.as_view() , name='delete'),
]
