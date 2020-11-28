from django.urls import path, include
from . import views
urlpatterns = [
    path('event', views.EventsAPI.as_view(), name='event'),

]
