from rest_framework import serializers

from cbsaas.banking.models import Wallet, WalletRecords, Transactions


class CreateWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("wallet_name", "scheme_code")


class AddWalletSerializer(serializers.Serializer):
    client_ref = serializers.CharField(allow_blank=False, max_length=100)
    wallet_name = serializers.CharField(allow_blank=False, max_length=100)
    scheme_code = serializers.CharField(allow_blank=False, max_length=100)


class WalletAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')


class WalletRecordsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletRecords
        fields = ('__all__')


class TransactionsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('__all__')