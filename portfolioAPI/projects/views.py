from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .serializers import ProjectSerializer, TagSerializer
from . models import Projects, Tags
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from . permissions import IsOwner
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


    def get_permissions(self):
        if self.action == 'list' or self.action == 'tags' or self.action == 'search':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsOwner, IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    # this functions is responsible for searching by tag
    # and then displaying the result of the search 
    @action(detail=False, methods=["GET"])
    def search(self, request, *args, **kwargs):
        #so lets send information based on a tag or word in the following manner
        # the tag query_param will check for tags while sentence will check the descriptions
        request_params = request.query_params
        if request_params:
            if request_params.get("tag", None) is not None:
                tag = request_params.get("tag")
                # now we check if the tag is a valid tag
                try:
                    # to make sure this does not result in an error we will use a try block
                    target_tag = Tags.objects.get(name = tag)
                    # now we have to search all the projects associated with this tag
                    associated_projects = target_tag.projects_set.all()
                    print(associated_projects)
                    serializer = ProjectSerializer(associated_projects, many=True)
                    return Response(serializer.data)
                except:
                    raise NotFound
        else:
            return self.list(request, *args, **kwargs)
    
    @action(detail=True, methods=["GET"])
    def tags(self, request, pk=None):
        # this function is responsible for showing just the tags associated with a project
        project = self.get_object()
        serializer = TagSerializer(project.tags, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # when the object is to be destroyed first archive the object
        object_instance = self.get_object()
        
        if object_instance.archive == False:
            object_instance.archive = True
            object_instance.save()
            return super().list(request, *args, **kwargs)
        else:
            return super().destroy(request, *args, **kwargs)
            
       
        # if the object is already archived then delete the object permanently


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tags.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

