from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from accounts.models import AccountUsers


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    # is_active = serializers.BooleanField(default=False, read_only=True)

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
        if request.user.is_authenticated:
            validated_data['owner'] = self.context['request'].user

        validated_data['is_active'] = False
        password = validated_data.pop('password')
        user = AccountUsers.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
