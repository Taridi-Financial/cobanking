from django.contrib.auth import get_user_model
from cbsaas.cin.services.operations import get_consumer
from cbsaas.ibase.services.helpers import format_response
from cbsaas.users.models import Members, Staff
from rest_framework import status
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .serializers import AddUserSerializer, MemberSerializer, UserSerializer, ViewUserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_user(request):
    client_id = request.data.get("client_id", None)
    add_user_serializer = AddUserSerializer(data=request.data)
    if not add_user_serializer.is_valid():
        return format_response(code=400, message=add_user_serializer.errors)
    
    if not add_user_serializer.is_valid():
        consumer_number = add_user_serializer.data["consumer_number"]
        consumers_get_or_check_nn(client_id=None, consumer_national_no=None, owner_type=None, request_type=None, get_pk=False)
        consumer = get_consumer(consumer_number=consumer_number, client_id=client_id, consumer_type='USER')
        if not consumer:
            return format_response(code=400, message={'msg': 'Sorry consumer with that number does not exist'})
        user_type = add_user_serializer.data["email"] #member, staff
        email = add_user_serializer.data["email"]
        phone = add_user_serializer.data["email"]
        staff_or_member_no= add_user_serializer.data["email"]
        gender = add_user_serializer.data["email"]
        DOB = add_user_serializer.data["email"]
        marital_status = add_user_serializer.data["email"]
        new_user = User.objects.create_user(
            username=email, 
            email=email, 
            name=consumer.consumer_name, 
            consumer_id=consumer.id,
            password="", 
            is_active=False,
            phone=phone,
            gender=gender,
            marital_status=marital_status,
            DOB=DOB
        )

        if user_type == "staff":
            Staff.objects.create(client_id=client_id,user_id=new_user.id, staff_id=staff_or_member_no)
    
        else:
            Members.objects.create(client_id=client_id,user_id=new_user.id, membership_no=staff_or_member_no)

        

        # email = serializer.data["email"]
        # name = serializer.data["name"]
        # password = serializer.data["password"]

        # new_user = User.objects.create_user(
        #     username=email, email=email, name=name, password=password, is_active=False
        # )

        # serializer = ViewUserSerializer(new_user)
        # return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["POST"])
@authentication_classes([])
@api_view(['GET'])
def members_list(request):
    client_id = request.data.get("client_id", None)
    if request.method == "GET":
        status = request.GET.get('status', None)
        if not status:
            member_qs = Members.objects.tenant_querry(client_id=client_id).all().order_by("-id")
        else:
            member_qs = Members.objects.tenant_querry(client_id=client_id).filter(status=status).order_by("-id")

        member_serializers = MemberSerializer(member_qs, many=True)
        return format_response(code=200, message=member_serializers.data)




@api_view(['GET', 'PUT', 'DELETE'])
def member_get_or_update(request, pk):
    client_id = request.data.get("client_id", None)
    pass
    # branch = tenant_get_model(client_id=client_id, pk=pk, model_name="branches")
    # if not branch:
    #     return format_response(code=400, message="Branch not found")
    # if request.method == "GET":
    #     branch_serializer = BranchViewSerializer(branch)
    #     return format_response(code=200, message=branch_serializer.data)
    # if request.method == "PUT":
    #     branch_serializer = BranchEditSerializer(instance=branch, data=request.data)
    #     branch_serializer.is_valid(raise_exception=True)
    #     branch_serializer.save()
    #     return format_response(code=200, message=branch_serializer.data)
    # if request.method == "DELETE":
    #     branch.delete()
    #     return format_response(code=204, message={'msg': 'done'})