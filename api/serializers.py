from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models import User


class ManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'password', 'owner',
        )
        read_only_fields = ('is_active', 'owner')

    def validate_email(self, value):
        users = User.objects.filter(email=value, is_active=True)
        if self.instance is not None:
            users = users.exclude(pk=self.instance.pk)
        if users.exists():
            raise serializers.ValidationError(_('This email address is already used!'))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
