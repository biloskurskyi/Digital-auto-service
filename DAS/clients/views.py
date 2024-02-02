from common.views import ClientCreateView, ClientUpdateView, ClientDeleteView


class ClientOwnerCreateView(ClientCreateView):
    template_name = 'clients/owner_create_client.html'
    path_name = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class ClientManagerCreateView(ClientCreateView):
    template_name = 'clients/manager_create_client.html'
    path_name = 'manager_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None


class ClientOwnerUpdateView(ClientUpdateView):
    template_name = 'clients/owner_client.html'
    path_name = 'client_owner'


class ClientManagerUpdateView(ClientUpdateView):
    template_name = 'clients/manager_client.html'
    path_name = 'client_manager'


class OwnerClientAccountDelete(ClientDeleteView):
    template_name = 'clients/delete_owner_client.html'
    reverse_page = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user.owner


class ManagerClientAccountDelete(ClientDeleteView):
    template_name = 'clients/delete_manager_client.html'
    reverse_page = 'manager_profile'

    def check_access(self, request, profile_user):
        return profile_user.owner == request.user.owner
