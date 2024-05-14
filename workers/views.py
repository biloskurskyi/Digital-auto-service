from common.views import (ClientDeleteView, WorkerCreateView, WorkerDeleteView,
                          WorkerUpdateView)
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


class WorkerOwnerUpdateView(WorkerUpdateView):
    template_name = 'workers/owner_worker.html'
    creator_type = 'owner'
    reverse_page = path_name = 'worker_owner'
    paginate_by = 3

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     workers = Worker.objects.all()
    #     paginator = Paginator(workers, 3)  # 10 workers per page
    #     page = self.request.GET.get('page')
    #     try:
    #         workers = paginator.page(page)
    #     except PageNotAnInteger:
    #         workers = paginator.page(1)
    #     except EmptyPage:
    #         workers = paginator.page(paginator.num_pages)
    #     context['workers'] = workers
    #     return context

    # def get_workers_query(self):
    #     if self.creator_type == 'owner':
    #         owner = self.request.user if self.request.user.owner is None else self.request.user.owner
    #         return Worker.objects.filter(owner=owner)


class WorkerManagerUpdateView(WorkerUpdateView):
    template_name = 'workers/manager_worker.html'
    creator_type = 'manager'
    reverse_page = path_name = 'worker_manager'


class WorkerOwnerDeleteView(WorkerDeleteView):
    template_name = 'workers/owner_delete_worker.html'
    reverse_page = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user.owner


class WorkerManagerDeleteView(WorkerDeleteView):
    template_name = 'workers/manager_delete_worker.html'
    reverse_page = 'manager_profile'

    def check_access(self, request, profile_user):
        return profile_user.owner == request.user.owner
