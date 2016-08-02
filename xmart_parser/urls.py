from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from projects import views
from projects.urls import *

urlpatterns = [
    url(r'^api/work_files/$', work_files_list, name='work-files-list'),
    url(r'^api/work_files/(?P<pk>[0-9]+)/$', work_files_detail, name='work-files-detail'),
    url(r'^api/uploaded_files/$', uploaded_files_list, name='uploaded-files-list'),
    url(r'^api/uploaded_files/(?P<pk>[0-9]+)/$', uploaded_files_detail, name='uploaded-files-detail'),
    url(r'^api/projects/$', project_list, name='project-list'),
    url(r'^api/projects/(?P<pk>[0-9]+)/$', project_detail, name='project-detail'),
    url(r'^api/change_pass/$', views.change_pass),
    url(r'^api/upload_file/$', views.upload_file),
    url(r'^api/process_all/$', views.process_all),
    url(r'^api/api-token-auth/', obtain_jwt_token),
    url(r'^api/admin/', admin.site.urls),
]
