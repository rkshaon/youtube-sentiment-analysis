from django.urls import path

from youtube import views


urlpatterns = [
    path('', views.index, name='index'),
]