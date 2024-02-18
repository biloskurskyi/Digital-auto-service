from common.views import WorkerCreateView
from orders.models import Order


class WorkerOwnerCreateView(WorkerCreateView):
    template_name = 'workers/owner_create_worker.html'
    path_name = 'owner_profile'
    creator_type = 'owner'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None

    # def get_queryset(self):
    #     print(self.request.user)
    #     worker_owner_id = self.request.user.id
    #     return Order.objects.filter(client__owner_id=worker_owner_id)


class WorkerManagerCreateView(WorkerCreateView):
    template_name = 'workers/manager_create_worker.html'
    path_name = 'manager_profile'
    creator_type = 'manager'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None
