# this is something that improves the process of send and convert object from end to end
from rest_framework import serializers
from .models import User, Transaction

class TransactionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class UserSerializer (serializers.ModelSerializer):
    transactions = TransactionSerializer (many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'balance', 'transactions']