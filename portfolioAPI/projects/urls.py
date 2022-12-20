from django.urls import path, include
from . import views
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter




# let create a router
router = DefaultRouter()
router.register("projects", viewset=views.ProjectViewSet, basename="projects")
router.register("tags", viewset=views.TagViewSet, basename="tags")



urlpatterns = [
    path("auth/token", view = views.TokenObtainPairView.as_view(), name="token"),
    path("auth/refresh", view = views.TokenRefreshView.as_view(), name="refresh"),
    path("", include(router.urls)),

]