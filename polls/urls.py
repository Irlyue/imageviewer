from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('image/id/<int:idx>', views.image_id, name='image_id'),
    path('image/name/<str:name>', views.image_name, name='image_name'),

]