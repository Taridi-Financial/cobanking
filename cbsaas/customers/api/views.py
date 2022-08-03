from cbsaas.customers.services.operations import get_user_code
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cbsaas.customers.api.serializers import CustomersAddSerializer, CustomersAllSerializer, TempCustomersAllSerializer
from cbsaas.customers.models import Customers, TempCustomers

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_customer(request):
    serializer = CustomersAddSerializer(data=request.data)
    if serializer.is_valid():
        client_ref=request.data.get('client_ref', None)

        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        email = serializer.data.get('email', None)
        phone = serializer.data.get('phone', None)
        physical_address = serializer.data.get('physical_address', None)

        temp_customer = TempCustomers(first_name=first_name, last_name=last_name, email=email, phone =phone, physical_address=physical_address )
        temp_customer.type = "new"
        temp_customer.client_id = 1
        temp_customer.made_by = get_user_code()
        temp_customer.status = "enter"
        temp_customer.save()

        return Response(
                {"status": 0, "message": "Added successfully, wait for approval"}, status=HTTP_200_OK
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def update_customer(request):
    serializer = CustomersAllSerializer(data=request.data)
    if serializer.is_valid():
        instance_id=request.data.get('id', None)

        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        email = serializer.data.get('email', None)
        phone = serializer.data.get('phone', None)
        physical_address = serializer.data.get('physical_address', None)
        client = serializer.data.get('client_ref', None)

        temp_customer = TempCustomers(first_name=first_name, last_name=last_name, email=email, phone =phone, physical_address=physical_address )
        temp_customer.type = "new"
        temp_customer.made_by = get_user_code()
        temp_customer.status = "enter"
        temp_customer.instance_id = instance_id
        temp_customer.save()

        return Response(
                {"status": 0, "message": "Updated successfully, wait for approval"}, status=HTTP_200_OK
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def approve_customer(request):
    change_details_id=request.data.get('temp_cust_id', None)
    action=request.data.get('action', None) #approve, reject
    try:
        temp_customer = TempCustomers.objects.get(id=change_details_id)
    except:
        print("pass")
    else:
        if action == "reject":
            temp_customer.delete()
        elif action == "approve":
            if temp_customer.type == "new":

                new_customer = Customers()
                new_customer.first_name = temp_customer.first_name
                new_customer.last_name = temp_customer.last_name
                new_customer.email = temp_customer.email
                new_customer.phone = temp_customer.phone 
                new_customer.physical_address = temp_customer.physical_address
                new_customer.client = temp_customer.client  
                new_customer.save()
                temp_customer.delete()
            else:
                customer = TempCustomers.objects.get(id=change_details_id)
                customer.first_name = temp_customer.first_name
                customer.save()
            

        return Response({"status": 0, "message": "Updated successfully, wait for approval"}, status=HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def delete_customer(request):
    """TO DO Delete"""
    return Response(
                {"status": 0, "message": "Updated successfully, wait for approval"}, status=HTTP_200_OK
            )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_all_customers(request):
    customers = Customers.objects.all()
    serializer = CustomersAllSerializer(customers, many=True)
    return Response({'customers': serializer.data},
                    status=HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_pending_customers(request):
    customers = TempCustomers.objects.all()
    serializer = TempCustomersAllSerializer(customers, many=True)
    return Response({'temp_customers': serializer.data},
                    status=HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_pending_customer(request, id):
    customer = TempCustomers.objects.get(id=id)
    serializer = TempCustomersAllSerializer(customer)
    return Response({'temp_customer': serializer.data},
                    status=HTTP_200_OK)