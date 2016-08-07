from projects.models import Projects


class ActiveProject(object):

    def process_request(self, request):
        id = request.COOKIES.get('id_project')
        if Projects.objects.filter(id=id).exists():
            project = Projects.objects.get(id=id)
        else:
            project = Projects.objects.all().first()
        if project:
            request.project = project
