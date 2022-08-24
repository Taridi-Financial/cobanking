from cbsaas.ibase.services.authorities import has_view_rights
from cbsaas.lending.api.serializers import ApplyMobileLoanSerializer, CreateMobileLoanProductChargeSerializer, CreateMobileLoanProductSerializer, RepayMobileLoanSerializer
from cbsaas.lending.services.operations import MobileLoansOperations
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST



@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
@has_view_rights
def apply_loan(request):
    serializer = ApplyMobileLoanSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.data['phone_number']
        client_ref = serializer.data['client_ref']
        amount = serializer.data['amount']
        loan_code = serializer.data['loan_code']
        disburse_wallet = request.data['disburse_wallet']
    
        mobile_ln_ops =MobileLoansOperations(phone_number=phone_number,  client_ref=client_ref, amount=amount, loan_code=loan_code)
        batch_resp = mobile_ln_ops.apply_loan(disburse_wallet=disburse_wallet)
      
        return Response({"status": "action_status", "message": batch_resp }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def repay_loan(request):
    serializer = RepayMobileLoanSerializer(data=request.data)
    if serializer.is_valid():
        loan_ref = serializer.data['loan_ref']
        amount= serializer.data['amount']
        source_wlt = serializer.data['source_wlt']

        mobile_ln_ops =MobileLoansOperations(loan_ref=loan_ref)
        repay_resp = mobile_ln_ops.repay_loan(source_wlt =source_wlt, amount=amount)

        return Response({"status": "action_status", "message": repay_resp }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def create_loan_product(request):
    serializer = CreateMobileLoanProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "action_status", "message": "" }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_loan_product_charge(request):
    serializer = CreateMobileLoanProductChargeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "action_status", "message": "" }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)