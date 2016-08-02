from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Projects(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()

class UploadedFiles(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    filename = models.TextField()
    description = models.TextField()
    network = models.TextField()
    filetype = models.TextField()
    vendor = models.TextField()

class WorkFiles(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    filename = models.TextField()
    description = models.TextField()
    network = models.TextField()
    filetype = models.TextField()
    vendor = models.TextField()
