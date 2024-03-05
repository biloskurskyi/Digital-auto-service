from django.shortcuts import render
from requests import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import AccountUsers
from accounts.serializer import AccountSerializer


class AccountViewSet(ModelViewSet):
    queryset = AccountUsers.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(AccountViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'GET':  # and self.request.user.owner is None
            queryset = AccountUsers.objects.filter(owner=self.request.user)
        return queryset
