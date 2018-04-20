from django.conf.urls import url
from app import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vsyo-budet', views.ok, name='ok')
]
