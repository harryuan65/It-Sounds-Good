from django.urls import path
from . import views

urlpatterns = [
  # path('', views.home ,name='index'),
  path('', views.render_index,name='render_index'),
  # path('upload_file', views.upload_file,name='upload_file'),
  path('send_json', views.send_json ,name='send_json'),
]