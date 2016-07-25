from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from projects.serializers import ProjectsSerializer
from projects.models import Projects
from rest_framework import permissions


class ProjectsList(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST', ])
def change_pass(request):
    user = request.user
    old_pass = request.data.get('old_pass')
    new_pass = request.data.get('new_pass')
    if user.check_password(old_pass):
        user.set_password(new_pass)
        user.save()
    return Response([])
