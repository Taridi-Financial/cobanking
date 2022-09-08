from cbsaas.lending.models import LoanProduct, LoanProductCharges, Loan
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

class RepayLoanerializer(serializers.Serializer):
    loan_ref = serializers.CharField(allow_blank=False, max_length=100)
    amount= serializers.CharField(allow_blank=False, max_length=100)
    source_wlt =serializers.CharField(allow_blank=False, max_length=100) 

class ApproveLoanerializer(serializers.Serializer):
    loan_ref = serializers.CharField(allow_blank=False, max_length=100)
    action= serializers.CharField(allow_blank=False, max_length=100)

class WalletAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')

class CreateLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = ('__all__')

class LoanAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('__all__')

class CreateLoanProductChargeserializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProductCharges
        fields = ('__all__')