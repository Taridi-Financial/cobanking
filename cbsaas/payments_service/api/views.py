from cbsaas.parameters.services.operations import add_wallet_for_code_type
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def test_disbursment(request):
    print('ggggggggggggggggggggggggttttttttttttttttttttttttttttttkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    print(request.data)
    return Response({"status": "action_status", "message": "message" }, status=HTTP_200_OK )
       
        
    # return Response(
    #     {"status": action_status, "message": message,},
    #     status=HTTP_400_BAD_REQUEST,
    # )
      

    # return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)