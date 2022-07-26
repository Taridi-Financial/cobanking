from rest_framework import serializers

from cbsaas.banking.models import LedgerWallet


class CreateLedgerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWallet
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



class LedgerWalletAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWallet
        fields = ('__all__')