from common.views import CarCreateView, CarDeleteView, CarUpdateView


class CarOwnerCreateView(CarCreateView):
    reverse_page = 'owner_profile'
    creator_type = 'owner'
    template_name = 'cars/owner_create_car.html'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class CarManagerCreateView(CarCreateView):
    reverse_page = 'manager_profile'
    creator_type = 'manager'
    template_name = 'cars/manager_create_car.html'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None


class CarOwnerUpdateView(CarUpdateView):
    template_name = 'cars/owner_car.html'
    creator_type = 'owner'
    reverse_page = path_name = 'car_owner'


class CarManagerUpdateView(CarUpdateView):
    template_name = 'cars/manager_car.html'
    creator_type = 'manager'
    reverse_page = path_name = 'car_manager'


class OwnerCarAccountDelete(CarDeleteView):
    template_name = 'cars/owner_delete_car.html'
    reverse_page = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user.client.owner


class ManagerCarAccountDelete(CarDeleteView):
    template_name = 'cars/manager_delete_car.html'
    reverse_page = 'manager_profile'

    def check_access(self, request, profile_user):
        return profile_user.client.owner == request.user.owner
