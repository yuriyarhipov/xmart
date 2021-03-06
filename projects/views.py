from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from projects.serializers import ProjectsSerializer, UploadedFilesSerializer, WorkFilesSerializer
from projects.models import Projects, UploadedFiles, WorkFiles, Tables
from rest_framework import permissions
from tempfile import mkdtemp
from multiprocessing import Process, Pool
from os.path import join
from projects.parser import Parser
import pandas as pd
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.gzip import gzip_page
from pyexcelerate import Workbook



pool = Pool(processes=1)

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

    def get_queryset(self):
        return UploadedFiles.objects.filter(project=self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project.name)

class WorkFilesViewSet(viewsets.ModelViewSet):
    serializer_class = WorkFilesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return WorkFiles.objects.filter(project=self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project.name)


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
        project = request.project,
        filename = filename,
        description = request.POST.get('description'),
        network = request.POST.get('network'),
        filetype = request.POST.get('file_type'),
        vendor = request.POST.get('vendor')
    )
    return Response([])


@api_view(['POST', ])
def process_all(request):
    for uf in UploadedFiles.objects.filter(project=request.project):
        pool.apply_async(Parser().parse_file, (uf, ))                
    return Response([])


@api_view(['GET', ])
def by_technology(request, vendor, network):
    result = set()
    project = request.project
    for t in Tables.objects.filter(vendor=vendor, network=network, workfile__project=project):
        result.add(t.table)
    result = list(result)
    result.sort()
    return Response(result)

@api_view(['GET', ])
@gzip_page
def table(request, table):
    data = []
    for table in Tables.objects.filter(table=table, workfile__project=request.project):
        data.extend(table.data)
    columns = list(data[0].keys())
    columns.sort()
    return Response({'data': data, 'columns': columns})

@api_view(['GET', ])
@permission_classes((AllowAny, ))
def get_excel(request):    
    tables = request.GET.getlist('table')        
    wb = Workbook()
    for table in tables:
        data = []
        columns = []
        for t in Tables.objects.filter(table=table, workfile__project=request.project):
            if len(t.data) > 0:
                columns.extend(t.data[0].keys())
                data.extend(t.data)
        columns = list(set(columns))
        columns.sort()
        excel_data = [columns, ]
        for row in data:
            r = []
            for col in columns:
                r.append(row.get(col))
            excel_data.append(r)
        wb.new_sheet(table, data=excel_data)
    wb.save('frontend/static/report.xlsx')        
    return HttpResponseRedirect('/static/report.xlsx')
