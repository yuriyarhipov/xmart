from rest_framework import serializers
from projects.models import Projects, UploadedFiles, WorkFiles
from django.contrib.auth.models import User

class ProjectsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Projects
        fields = ('id', 'name', 'user')


class UploadedFilesSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.name')
    class Meta:
        model = UploadedFiles
        fields = ('id', 'project', 'filename', 'description', 'network', 'filetype', 'vendor', )


class WorkFilesSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.name')
    class Meta:
        model = WorkFiles
        fields = ('id', 'project', 'filename', 'description', 'network', 'filetype', 'vendor', 'result')


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Projects.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
