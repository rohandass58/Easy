# incidents/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"incidents", views.IncidentViewSet, basename="incident")
urlpatterns = [
    path("", include(router.urls)),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
