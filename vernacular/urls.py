from django.urls import path, include
from . import views

urlpatterns = [
    path("finite_validator/", views.finitevalues.as_view(), name="finite"),
    path("numeric_validator/", views.numeric.as_view(), name="numeric"),

]