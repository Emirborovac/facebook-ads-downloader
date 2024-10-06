from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_video_view, name='download_video'),  # Updated to match the correct function name
]
