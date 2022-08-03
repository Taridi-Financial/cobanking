from rest_framework import serializers

from cbsaas.customers.models import Customers, TempCustomers


class CustomersAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('__all__')


class CustomersAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ("first_name", "last_name", "last_name", "email", "phone", "physical_address")


class TempCustomersAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempCustomers
        fields = ('__all__')