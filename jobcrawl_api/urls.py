from . import views
from django.urls import path

urlpatterns = [
    path('', views.crawler, name='crawler'),
]
