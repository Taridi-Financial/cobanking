from rest_framework import serializers

from ..models import Clients


class ClientsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"


class ClientsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ("address", "client_name", "identifying_number")
