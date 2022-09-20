from django.test import TestCase
from cbsaas.cin.models import ConsumerRegistry

from cbsaas.clients.models import Clients
from cbsaas.lending.models import LoanProduct
from cbsaas.lending.services.operations import LoanOperations

def TestLoanOperations(TestCase):

    def setUp(self):
        # Setup run before every test method.
        Clients.objects.create(client_name='Big', identifying_number=1234, address="dd")
        ConsumerRegistry.objects.create(national_number='123', client_ref=self.client.client_ref)
        LoanProduct.objects.create(client_id=1, 
                                    loan_code="TB100",
                                    loan_type="mobile" , 
                                    description ="",
                                    duration = 60,
                                    upper_limit = 2000,
                                    interest_realization = "prorated",
                                    loan_period = 60,
                                    penalty_period =60,
                                    penalty_grace_period = 10)

        ConsumerRegistry.objects.create(national_number='123', client_ref=self.client.client_ref)

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_loan_limit():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass

    def test_apply_loan():
        """TO DO: Test that the loan can be applied and set to pending"""
        client_ref  = Clients.objects.get(id=1)
        loan_ops = LoanOperations(client_ref=None, amount=1000, loan_code=None,phone_number=None,consumer=None, action_by=None, loan_type = "mobile")
    


def TestLoanAmotization(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_amotization_creation():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass

    def test_amotization_creation():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass


def TestSecuringLoans(TestCase):

    def setUp(self):

        self.client = Clients.objects.create(client_name='Big', identifying_number=1234, address="dd")
        
        self.consumer = ConsumerRegistry.objects.create(national_number='123', client_ref=self.client.client_ref)
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_amotization_creation():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass