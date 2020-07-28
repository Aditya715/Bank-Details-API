from django.contrib.auth.models import User
from rest_framework import serializers
from .models import BankDetail

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ['bank_name', 'ifsc_code', 'branch_name', 'branch_address']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']