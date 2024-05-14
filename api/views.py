from datetime import timedelta
import uuid

from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied, ValidationError
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

    # def get_permissions(self):
    #     # if self.action in ('partial_update',):
    #     #     self.permission_classes = (IsAdminUser,)
    #     if self.action in ('create',):
    #         return []
    #     return super(AccountViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'GET':  # and self.request.user.owner is None
            queryset = AccountUsers.objects.filter(owner=self.request.user)

        return queryset

    def perform_destroy(self, serializer):
        profile_user = get_object_or_404(AccountUsers, pk=self.kwargs['pk'])
        if (
                self.request.method == 'DELETE' and
                self.request.user == profile_user and
                self.request.user.is_active and
                self.request.user.owner is None
        ):
            # serializer.delete()
            if self.request.user == profile_user:
                manager_user = AccountUsers.objects.filter(owner=profile_user)
                manager_user.delete()
            serializer.delete()
        else:
            raise PermissionDenied("You don't have permission to perform this action.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email(serializer.validated_data['password'])
        user.is_active = False
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        profile_user = get_object_or_404(AccountUsers, pk=self.kwargs['pk'])
        if (
                (self.request.method in ['PUT', 'PATCH']) and
                (self.request.user == profile_user or self.request.user == profile_user.owner) and
                self.request.user.is_active
        ):
            print(111)
            if 'password' in serializer.validated_data:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

            if 'username' in serializer.validated_data:
                username = serializer.validated_data['username']
                user_with_same_username = AccountUsers.objects.exclude(pk=profile_user.pk).filter(username=username)
                if user_with_same_username.exists():
                    if user_with_same_username.filter(is_active=True).exists():
                        raise ValidationError({'username': ['Username already exists.']})

            if 'phone' in serializer.validated_data:
                phone = serializer.validated_data['phone']
                if AccountUsers.objects.exclude(pk=profile_user.pk).filter(phone=phone, is_active=True).exists():
                    raise ValidationError({'phone': ['Phone number already exists.']})

            if 'email' in serializer.validated_data:
                new_email = serializer.validated_data['email']
                if new_email != profile_user.email:  # Check if the new email is different
                    # Check if the new email is already used by another user
                    if AccountUsers.objects.exclude(pk=profile_user.pk).filter(email=new_email,
                                                                               is_active=True).exists():
                        print('-')
                        raise ValidationError({"email": ["This email address is already used!!"]})

                # Assign the current user's email if 'email' field is not being updated
            serializer.instance = profile_user
            serializer.save(partial=True)
        else:
            raise PermissionDenied("You don't have permission to perform this action.")

# def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#
#     expiration = now() + timedelta(hours=24)
#     record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
#     record.send_verification_email(serializer.validated_data['password'])
#     user.is_active = False
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
