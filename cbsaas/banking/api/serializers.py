from rest_framework import serializers

from cbsaas.banking.models import LedgerWallet


class CreateLedgerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerWallet
        fields = ("wallet_name", "scheme_code", "wallet_type")
