from django.urls import path

from . import views

urlpatterns = [
    path('result', views.search, name='search'),
    path('health', views.health, name='health'),
    path('', views.index, name='index'),
]
