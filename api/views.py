from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ModelViewSet

from accounts import services
from accounts.models import User

from .serializers import ManagerSerializer


class AuthTokenView(ObtainAuthToken):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'token'


class ManagerViewSet(ModelViewSet):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return User.objects.for_tenant(user).order_by('pk')
        return User.objects.filter(Q(owner=user) | Q(pk=user.pk))

    def perform_create(self, serializer):
        if self.request.user.owner_id is not None:
            raise PermissionDenied
        user = serializer.save(owner=self.request.user)
        services.send_verification(self.request, user)

    def perform_destroy(self, instance):
        if instance != self.request.user or instance.owner_id is not None:
            raise PermissionDenied
        services.delete_owner_account(instance)
