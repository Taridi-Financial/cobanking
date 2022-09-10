from cbsaas.ibase.services.helpers import format_response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..models import CINRegistry
from .serializers import AddCINSerializer, ViewCINSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_cin(request):
    cin_number = request.data.get("cin")
    cin = CINRegistry.objects.filter(cin=cin_number).first()
    if cin:
        return format_response(code=400, message="serializer.errors")
    serializer = AddCINSerializer(data=request.data)
    if not serializer.is_valid():
        return format_response(code=400, message=serializer.errors)
        # return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({"cin_details": serializer.data}, status=HTTP_200_OK)

        
@api_view(["POST"])
def view_cin(request):
    cin_number = request.data.get("cin")
    try:
        cin = CINRegistry.objects.get(cin=cin_number)
    except Exception:
        pass
    else:
        serializer = ViewCINSerializer(cin)
        return Response({"cin_details": serializer.data}, status=HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_all_cin(request):
    cins = CINRegistry.objects.all()
    serializer = ViewCINSerializer(cins, many=True)
    return Response({"cins_details": serializer.data}, status=HTTP_200_OK)
