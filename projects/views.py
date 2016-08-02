from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from projects.serializers import ProjectsSerializer, UploadedFilesSerializer, WorkFilesSerializer
from projects.models import Projects, UploadedFiles, WorkFiles
from rest_framework import permissions
from tempfile import mkdtemp
from multiprocessing import Process
from os.path import join
from projects.parser import Parser



class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UploadedFilesViewSet(viewsets.ModelViewSet):
    queryset = UploadedFiles.objects.all()
    serializer_class = UploadedFilesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(project=Projects.objects.filter().first().name)

class WorkFilesViewSet(viewsets.ModelViewSet):
    queryset = WorkFiles.objects.all()
    serializer_class = WorkFilesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(project=Projects.objects.filter().first().name)


@api_view(['POST', ])
def change_pass(request):
    user = request.user
    old_pass = request.data.get('old_pass')
    new_pass = request.data.get('new_pass')
    if user.check_password(old_pass):
        user.set_password(new_pass)
        user.save()
    return Response([])

@api_view(['POST', ])
def upload_file(request):
    path = mkdtemp(suffix='_xmart')
    uploaded_file = request.FILES['file']
    filename = join(path, uploaded_file.name)
    with open(filename, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    UploadedFiles.objects.create(
        project = Projects.objects.filter().first(),
        filename = filename,
        description = request.POST.get('description'),
        network = request.POST.get('network'),
        filetype = request.POST.get('file_type'),
        vendor = request.POST.get('vendor')
    )
    return Response([])


@api_view(['POST', ])
def process_all(request):
    for uf in UploadedFiles.objects.all():
        p = Process(target=Parser().parse_file, args=(uf,))
        p.start()
    return Response([])
