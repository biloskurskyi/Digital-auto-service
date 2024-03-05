from rest_framework import fields, serializers

from accounts.models import AccountUsers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUsers
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')
