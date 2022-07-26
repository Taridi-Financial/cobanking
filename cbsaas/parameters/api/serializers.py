from cbsaas.parameters.models import ClientWalletDirectory
from rest_framework import serializers



class ClientWalletDirectoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWalletDirectory
        fields = "__all__"
