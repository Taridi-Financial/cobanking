from webbrowser import get
from cbsaas.ibase.services.authorities import has_view_rights
from cbsaas.ibase.services.helpers import format_response, get_cin_from_number
from cbsaas.lending.api.serializers import ApplyMobileLoanSerializer, ApproveLoanerializer, CreateLoanProductChargeserializer, CreateLoanProductSerializer, LoanAllSerializer, RepayLoanerializer
from cbsaas.lending.models import Loan
from cbsaas.lending.services.operations import LoanOperations, loans_apply_loan
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST



@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
@has_view_rights
def apply_loan(request) -> str:
    """
        For mobile applications the person who applies is the person set as the applicant. 
        For protal applications the person who applies is not the applicant. 
    """
    client_id = request.data.get("client_id", None)
    serializer = ApplyMobileLoanSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    phone_number = serializer.data['phone_number']
    action_by = request.user
    amount = serializer.data['amount']
    loan_code = serializer.data['loan_code']
    disburse_wallet = request.get('disburse_wallet', None)
    consumer_number=request.data.get('consumer_number')
    resp = loans_apply_loan(phone_number=phone_number,  client_id=client_id, amount=amount, loan_code=loan_code, action_by=action_by,disburse_wallet =disburse_wallet, consumer_number=consumer_number)
    return Response({"status": "action_status", "message": resp }, status=HTTP_200_OK)
    


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def request_to_repay_loan(request):
    """Used by third parties to send request for stk push that ultimately leads to repayment of loan"""
    serializer = RepayLoanerializer(data=request.data)  
    if serializer.is_valid():
        loan_ref = serializer.data['loan_ref']
        amount= serializer.data['amount']
        source_wlt = serializer.data['source_wlt']

        mobile_ln_ops =LoanOperations(loan_ref=loan_ref)
        repay_resp = mobile_ln_ops.repay_loan(source_wlt =source_wlt, amount=amount)

        return Response({"status": "action_status", "message": repay_resp }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def manual_repay_loan(request):
    """Used by the portal to repay a loan manually. Goes throug immediately"""
    serializer = RepayLoanerializer(data=request.data)  
    if serializer.is_valid():
        loan_ref = serializer.data['loan_ref']
        amount= serializer.data['amount']
        source_wlt = serializer.data['source_wlt']

        mobile_ln_ops =LoanOperations(loan_ref=loan_ref)
        repay_resp = mobile_ln_ops.repay_loan(source_wlt =source_wlt, amount=amount)

        return Response({"status": "action_status", "message": repay_resp }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def approve_loan(request):
    serializer = ApproveLoanerializer(data=request.data)
    if not serializer.is_valid():
        return format_response(code=400, message=serializer.errors)
    loan_ref = serializer.data['loan_ref']
    action = serializer.data['action']
    mobile_ln_ops =LoanOperations(loan_ref=loan_ref,  action_by="wen")
    resp = mobile_ln_ops.approve(action_type=action, action_by="wen")
    return format_response(code=200, message=resp)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def close_loan(request):
    loan_ref = request.data['loan_ref']
    mobile_ln_ops =LoanOperations(loan_ref=loan_ref)
    resp = mobile_ln_ops.close_loan()
    response_status = resp["response_status"]
    if not response_status == 0:
        return format_response(code=200, message=resp)
    else:
        return format_response(code=400, message=resp)

    


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_loans(request, client_ref):
    """pass status as a request params, allowed values are all, disbursed, pending"""
    status = request.GET.get('status')
    
    if status =="all":
        loans = Loan.objects.filter(client_ref=client_ref).order_by("-id")
    else:
        loans = Loan.objects.filter(client_ref=client_ref, loan_status=status).order_by("-id")
    serializer = LoanAllSerializer(loans, many=True) 
    return format_response(code=200, message=serializer.data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_loan(request, loan_ref):
    """pass status as a request params, allowed values are all, disbursed, pending"""
    client_ref = request.headers.get('Client')
    
    try:
        loan = Loan.objects.tenant_querry(client_ref=client_ref).get(loan_ref=loan_ref)
    except Exception:
        return format_response(code=200, message={"message": "sorry loan does not exist"})
    serializer = LoanAllSerializer(loan) 
    return format_response(code=200, message=serializer.data)

    
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def create_loan_product(request):
    serializer = CreateLoanProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "action_status", "message": "" }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_loan_product_charge(request):
    serializer = CreateLoanProductChargeserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "action_status", "message": "" }, status=HTTP_200_OK)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_loan_security(request):
    serializer = ApproveLoanerializer(data=request.data)
    if not serializer.is_valid():
        return format_response(code=400, message=serializer.errors)
    loan_ref = serializer.data['loan_ref']
    action = serializer.data['action']
    mobile_ln_ops =LoanOperations(loan_ref=loan_ref,  action_by="wen")
    resp = mobile_ln_ops.approve(action_type=action, action_by="wen")
    return format_response(code=200, message=resp)