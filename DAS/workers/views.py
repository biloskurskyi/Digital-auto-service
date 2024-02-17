from common.views import WorkerCreateView


class WorkerOwnerCreateView(WorkerCreateView):
    template_name = 'workers/owner_create_worker.html'
    path_name = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class WorkerManagerCreateView(WorkerCreateView):
    template_name = 'workers/manager_create_worker.html'
    path_name = 'manager_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None
