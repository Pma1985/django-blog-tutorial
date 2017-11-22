from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^pile_cap/$', views.compute, name='pile_cap'),
]