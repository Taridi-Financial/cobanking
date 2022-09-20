from django.contrib.auth import get_user_model
from cbsaas.users.models import Members
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


# class AddUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "name", "password"]


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('client_id')

class MemberSerializer(serializers.ModelSerializer):
    related_user = UserAllSerializer(read_only=True, source='rater')
    class Meta:
        model = Members
        exclude = ('client_id')

    def to_representation(self, instance):
        # get the usual response as a dictionary
        representation = super().to_representation(instance)
        # pop the nested field and flatten
        user_details = representation.pop('related_user')
        representation.update(user_details)
        return representation


class AddUserSerializer(serializers.ModelSerializer):
    consumer_number = serializers.CharField()
    user_type = serializers.CharField() #member, staff
    email = serializers.CharField()
    phone = serializers.CharField()
    staff_or_member_no= serializers.CharField()
    gender = serializers.CharField()
    DOB = serializers.CharField()
    marital_status = serializers.CharField()
