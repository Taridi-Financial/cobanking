from cbsaas.ibase.services.authorities import has_view_rights
from cbsaas.ibase.services.helpers import format_response
from cbsaas.lending.api.serializers import ApplyMobileLoanSerializer, ApproveMobileLoanSerializer, CreateMobileLoanProductChargeSerializer, CreateMobileLoanProductSerializer, MobileLoansAllSerializer, RepayMobileLoanSerializer
from cbsaas.lending.models import MobileLoans
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
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    phone_number = serializer.data['phone_number']
    client_ref = serializer.data['client_ref']
    amount = serializer.data['amount']
    loan_code = serializer.data['loan_code']
    disburse_wallet = request.data['disburse_wallet']

    mobile_ln_ops =MobileLoansOperations(phone_number=phone_number,  client_ref=client_ref, amount=amount, loan_code=loan_code)
    resp = mobile_ln_ops.apply_loan(disburse_wallet=disburse_wallet)
    
    return Response({"status": "action_status", "message": resp }, status=HTTP_200_OK)
    


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def request_to_repay_loan(request):
    """Used by third parties to send request for stk push that ultimately leads to repayment of loan"""
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
def manual_repay_loan(request):
    """Used by the portal to repay a loan manually. Goes throug immediately"""
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
def approve_loan(request):
    serializer = ApproveMobileLoanSerializer(data=request.data)
    if not serializer.is_valid():
        return format_response(code=400, message=serializer.errors)
    loan_ref = serializer.data['loan_ref']
    action = serializer.data['action']
    mobile_ln_ops =MobileLoansOperations(loan_ref=loan_ref,  action_by="wen")
    resp = mobile_ln_ops.approve(action_type=action, action_by="wen")
    return format_response(code=200, message=resp)



@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_loans(request, client_ref):
    """pass status as a request params, allowed values are all, disbursed, pending"""
    status = request.GET.get('status')
    if status =="all":
        loans = MobileLoans.objects.filter(client_ref=client_ref).order_by("-id")
    else:
        loans = MobileLoans.objects.filter(client_ref=client_ref, loan_status=status).order_by("-id")
    serializer = MobileLoansAllSerializer(loans, many=True) 
    return format_response(code=200, message=serializer.data)

    
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