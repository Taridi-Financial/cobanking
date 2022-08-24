from rest_framework import serializers

from ..models import CINRegistry


class ViewCINSerializer(serializers.ModelSerializer):
    class Meta:
        model = CINRegistry
        fields = "__all__"


class AddCINSerializer(serializers.ModelSerializer):
    class Meta:
        model = CINRegistry
        fields = "__all__"

