from rest_framework import serializers
from projects.models import Projects
from django.contrib.auth.models import User

class ProjectsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Projects
        fields = ('id', 'name', 'user')



class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Projects.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
