from django.urls import path
from . import views

urlpatterns = [
  path('', views.index,name='index'),
  path('send_json', views.send_json ,name='send_json'),
]