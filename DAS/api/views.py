from datetime import timedelta
import uuid
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import AccountUsers, EmailVerification
from accounts.serializer import AccountSerializer


class AccountViewSet(ModelViewSet):
    queryset = AccountUsers.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        if self.action in ('create',):
            return []
        return super(AccountViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'GET':  # and self.request.user.owner is None
            queryset = AccountUsers.objects.filter(owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['is_active'] = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(is_active=False)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email(
            serializer.validated_data['password'])
        user.is_active = False  # Встановлюємо is_active на False перед збереженням користувача
        # for i in user:
        #     print(i)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
