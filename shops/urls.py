from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path(r'produkt/<int:pk>/', views.prod_dyqan, name="produkt"),
    path(r'dyqan/<int:pk>/', views.dyqan, name="dyqan"),
    path(r'bli/<int:pk>/', views.bli, name="bli"),
    path(r'porosite_e_mia/<int:pk>/hiq/', views.hiq, name="hiq"),
    path(r'regjistrohu/', views.regjistrohu, name="regjistrohu"),
    path(r'logini/', views.logini, name="logini"),
    path(r'logoutUser/', views.logoutUser, name="logoutUser"),
    path(r'dyqan/<int:pk>/inventar/', views.inventar, name="inventar"),
    path(r'paguaj/', views.paguaj, name="paguaj"),
    path(r'porosite_e_mia/', views.porosite_e_mia, name="porosite_e_mia"),

]

