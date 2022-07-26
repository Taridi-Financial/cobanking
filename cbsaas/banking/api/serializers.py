from rest_framework import serializers

from cbsaas.banking.models import LedgerWallet, LedgerWalletRecords


class CreateLedgerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWallet
        fields = ("wallet_name", "scheme_code")


class AddLedgerSerializer(serializers.Serializer):
    client_ref = serializers.CharField(allow_blank=False, max_length=100)
    wallet_name = serializers.CharField(allow_blank=False, max_length=100)
    scheme_code = serializers.CharField(allow_blank=False, max_length=100)


class LedgerWalletAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWallet
        fields = ('__all__')


class LedgerWalletRecordsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWalletRecords
        fields = ('__all__')