from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from projects import views

urlpatterns = [
    url(r'^api/projects/$', views.ProjectsList.as_view()),
    url(r'^api/change_pass/$', views.change_pass),
    url(r'^api/api-token-auth/', obtain_jwt_token),
    url(r'^api/admin/', admin.site.urls),
]
