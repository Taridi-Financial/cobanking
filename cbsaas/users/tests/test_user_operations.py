from django.test import TestCase

from cbsaas.clients.services.client_services import ClientOperations
from cbsaas.clients.models import Branches, Clients


class MemberTestCase(TestCase):
    
    def setUp(self):
        self.client_ops = ClientOperations(identifying_number=1234,client_name = "Taridi Financial Systems" )
        
    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_add_member(self):
        """Test that a new member can be created
            test that a corresponding user is created 
        """
        pass

    def test_update_member(self):
        """Test that a new member can be created"""
        pass

    def test_delete_member(self):
        """Test that a new member can be created"""
        pass