from django.urls import path
from .views import index, watermark


urlpatterns = [
    path('', index, name="index"),
    path('watermark', watermark, name='watermark')
]
