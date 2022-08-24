from django.contrib.auth import get_user_model
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

from .serializers import AddUserSerializer, UserSerializer, ViewUserSerializer

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
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data["email"]
        name = serializer.data["name"]
        password = serializer.data["password"]

        new_user = User.objects.create_user(
            username=email, email=email, name=name, password=password
        )

        serializer = ViewUserSerializer(new_user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):
    name = request.data["name"]
    password = request.data["password"]
    return Response(status=status.HTTP_200_OK, data="serializer.data")

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)