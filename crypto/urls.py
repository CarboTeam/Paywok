# Django
from django.urls import path
from django.views.generic import TemplateView

# Apps
from . import views

app_name = "crypto"

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
