from cbsaas.lending.models import MobileLoanProduct, MobileLoanProductCharges
from rest_framework import serializers

from cbsaas.banking.models import Wallet


class CreateWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("wallet_name", "scheme_code")
class ApplyMobileLoanSerializer(serializers.Serializer):
    phone_number= serializers.CharField(allow_blank=False, max_length=100)
    client_ref = serializers.CharField(allow_blank=False, max_length=100)
    amount= serializers.CharField(allow_blank=False, max_length=100)
    loan_code=serializers.CharField(allow_blank=False, max_length=100)

class RepayMobileLoanSerializer(serializers.Serializer):
    loan_ref = serializers.CharField(allow_blank=False, max_length=100)
    amount= serializers.CharField(allow_blank=False, max_length=100)
    source_wlt =serializers.CharField(allow_blank=False, max_length=100) 

class WalletAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')

class CreateMobileLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileLoanProduct
        fields = ('__all__')

class CreateMobileLoanProductChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileLoanProductCharges
        fields = ('__all__')