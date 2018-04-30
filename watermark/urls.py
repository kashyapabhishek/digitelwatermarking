from django.urls import path
from .views import index,imageRetrive

urlpatterns = [
    path('', index, name="index"),
    path('retrive', imageRetrive, name="imageRetrive"),

]
