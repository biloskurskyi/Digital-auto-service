from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from accounts.models import AccountUsers


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AccountUsers
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'password', 'owner')

    def validate_email(self, value):
        if AccountUsers.objects.filter(email=value, is_active=True, is_verified_email=True).exists():
            raise serializers.ValidationError("This email address is already used!")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            validated_data['owner'] = None
        elif request.user.is_authenticated and request.user.owner is None:
            validated_data['owner'] = self.context['request'].user
        else:
            raise PermissionDenied("You don't have permission to perform this action.")

        validated_data['is_active'] = False
        password = validated_data.pop('password')
        user = AccountUsers.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def perform_update(self, instance, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticate:
            raise PermissionDenied("You don't have permission to perform this action.")


