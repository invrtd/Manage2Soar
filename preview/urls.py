"""URLs for the unlisted public-site preview.

Mounted by the project at ``preview/``.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="public_preview_home"),
    path("<slug:slug>/", views.page, name="public_preview_page"),
]
