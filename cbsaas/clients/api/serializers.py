from rest_framework import serializers

from ..models import Clients


class ClientsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"


class ClientsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ("identifying_number",  "client_name", "address")


class ClientsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ( "client_name", "address")
