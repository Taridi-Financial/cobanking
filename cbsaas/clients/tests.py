from http import client
from django.test import TestCase

from cbsaas.clients.services.client_services import ClientOperations
from cbsaas.clients.models import Branches, Clients


class ClientsTestCase(TestCase):
    
    def setUp(self):
        self.client_ops = ClientOperations(identifying_number=1234,client_name = "Taridi Financial Systems" )
        
    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_client_creation(self):
        client_ops_msg = self.client_ops.create_client()
        client_created = Clients.objects.filter(identifying_number=1234).exists()
        self.assertIs(client_created, True)
        # self.assertContains(client_ops_msg, 'Client creation successful')

    def test_double_client_creation(self):
        client_ops2 = ClientOperations(identifying_number=1234,client_name = "Taridi Financial Systems" )
        client_ops_msg2 = client_ops2.create_client()
        client_count = Clients.objects.filter(identifying_number=1234).count()
        self.assertNotEqual(client_count, 2)
        self.assertContains(client_ops_msg2, 'Sorry, another client with the same number exists')

    def test_branch_creation(self):
        """Test client created and two branches added"""
        self.client_ops.create_client()
        branch_count = Branches.objects.filter(client_id=1).count()
        self.assertEqual(branch_count, 2)
        branch_one = Branches.objects.filter(id=1).first()
        self.assertIsNot(branch_one, None)
        self.assertEqual(branch_one.client, 1)

    def test_superadmin_creation(self):
        """Test client created and superadmin added"""
        # self.client_ops.create_client()
        # staff_count = Staff.objects.filter(client_id=1).count()
        # self.assertEqual(staff_count, 1)
        pass


class CconsumerTestCase(TestCase):
    
    def setUp(self):
        self.client_ops = ClientOperations(identifying_number=1234,client_name = "Taridi Financial Systems" )
        
    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_client_creation(self):
        client_ops_msg = self.client_ops.create_client()
        client_created = Clients.objects.filter(identifying_number=1234).exists()
        self.assertIs(client_created, True)