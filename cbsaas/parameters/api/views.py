from cbsaas.parameters.services.operations import add_wallet_for_code_type
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from cbsaas.parameters.api.serializers import ClientWalletDirectoryAddSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_wallet_for_code(request):
    serializer = ClientWalletDirectoryAddSerializer(data=request.data)
    if serializer.is_valid():
  
        branch_code = "000"
        wallet_name = ""

        use_level = "global"
        wallet_ref=serializer.data['wallet_ref']
        client_ref=serializer.data['client_ref']
        use_type_code=serializer.data['use_type_code']
        
        wallet_description=serializer.data['wallet_description']

        create_params_resp = add_wallet_for_code_type(
            wallet_ref=wallet_ref,
            client_ref=client_ref,
            use_type_code=use_type_code,
            description=wallet_description,
            branch_code=branch_code,
            update=False,
        )


        action_status = create_params_resp["status"]
        message = create_params_resp["message"]
       
        if action_status == 1:
            return Response(
                {"status": action_status, "message": message,},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"status": action_status, "message": message }, status=HTTP_200_OK
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)