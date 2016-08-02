from projects.views import ProjectsViewSet, UploadedFilesViewSet, WorkFilesViewSet

project_list = ProjectsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_detail = ProjectsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

uploaded_files_list = UploadedFilesViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

uploaded_files_detail = UploadedFilesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

work_files_list = WorkFilesViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

work_files_detail = WorkFilesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
