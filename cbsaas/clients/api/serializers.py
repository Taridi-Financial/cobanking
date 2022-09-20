from rest_framework import serializers

from ..models import Clients, Branches, ConsumerRegistry


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


class BranchViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        exclude = ("client_id")


class BranchEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ( "branch_name", "branch_code", "status")


class ConsumerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerRegistry
        exclude = ( "client_id")


class ConsumerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerRegistry
        exclude = ( "client_id", "consumer_system_no")

