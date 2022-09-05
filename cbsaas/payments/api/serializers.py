from cbsaas.payments.models import WalletPaymentsDetails
from rest_framework import serializers



class WalletPaymentsDetailsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletPaymentsDetails
        fields = "__all__"
