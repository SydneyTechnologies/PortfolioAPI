from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



# let create a router
router = DefaultRouter()
router.register("projects", viewset=views.ProjectViewSet, basename="projects")
router.register("tags", viewset=views.TagViewSet, basename="tags")


urlpatterns = [
    path("", include(router.urls)),
]