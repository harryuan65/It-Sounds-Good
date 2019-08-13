from django.urls import path
from . import views

urlpatterns = [
  path('', views.home ,name='index'),
  path('render_index', views.render_index,name='render_index'),
  path('send_json', views.send_json ,name='send_json'),

]