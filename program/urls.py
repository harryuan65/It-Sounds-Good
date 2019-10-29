from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('', views.index,name='index'),
  # path('separation/<path:wav_path>/', views.separation,name='separation'),
  path('send_json', views.send_json ,name='send_json'),
]