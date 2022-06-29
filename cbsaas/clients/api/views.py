from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..models import Clients
from ..services.operations import add_client
from .serializers import ClientsAddSerializer, ClientsAllSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_new_client(request):
    serializer = ClientsAddSerializer(data=request.data)
    if serializer.is_valid():
        client_name = serializer.data.get("client_name")
        address = serializer.data.get("address")
        identifying_number = serializer.data.get("identifying_number")
        add_client_res = add_client(
            client_name=client_name,
            address=address,
            identifying_number=identifying_number,
        )
        status = add_client_res["status"]
        message = add_client_res["message"]
        if status == 1:
            return Response(
                {"status": status, "message": message}, status=HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    "status": status,
                    "message": message,
                    "cin": add_client_res["cin"],
                    "client_ref": add_client_res["client_ref"],
                },
                status=HTTP_200_OK,
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_client(request, client_id):
    try:
        client = Clients.objects.get(id=client_id)
    except Exception:
        return Response(
            {"status": 1, "message": "Client not found"}, status=HTTP_400_BAD_REQUEST
        )
    else:
        serializer = ClientsAllSerializer(client)
        return Response({"client_details": serializer.data}, status=HTTP_200_OK)
