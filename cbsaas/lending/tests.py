from django.test import TestCase

from cbsaas.clients.models import Clients

def TestLoanOperations(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_loan_limit():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass


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
        
        self.cin = CINRegistry.objects.create(cin='123', client_ref=self.client.client_ref)
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_amotization_creation():
        """TO DO: Test that tha use can only apply below their test limit"""
        pass