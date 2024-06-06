
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
         # Create a user and get a JWT token
        self.user = User.objects.create_user(username='admin', password='1234')
        self.token = AccessToken.for_user(self.user)

        # Set the Authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_vendor_api(self):
        # Test create vendor endpoint
        response = self.client.post('/api/vendors/', {'name': 'Vendor 1', 'contact_details': 'Contact 1', 'address': 'Address 1', 'vendor_code': 'V001'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Test retrieve vendor endpoint
        response = self.client.get(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test update vendor endpoint
        response = self.client.put(f'/api/vendors/{vendor_id}/', {'name': 'Updated Vendor 1', 'contact_details': 'Updated Contact 1', 'address': 'Updated Address 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test delete vendor endpoint
        response = self.client.delete(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_purchase_order_api(self):
        # Create a vendor
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V001')

        # Test create purchase order endpoint
        response = self.client.post('/api/purchase_orders/', {'po_number': 'PO001', 'vendor': vendor.id, 'order_date': '2024-06-10', 'delivery_date': '2024-06-20', 'items': [{'name': 'Item 1', 'quantity': 1}], 'quantity': 1, 'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        po_id = response.data['id']

        # Test retrieve purchase order endpoint
        response = self.client.get(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test update purchase order endpoint
        response = self.client.put(f'/api/purchase_orders/{po_id}/', {'status': 'canceled'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test delete purchase order endpoint
        response = self.client.delete(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_vendor_performance_view(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V001')
        response = self.client.get(f'/api/vendors/{vendor.vendor_code}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order_view(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V001')
        purchase_order = PurchaseOrder.objects.create(vendor=vendor, po_number='PO001', order_date='2024-06-10', delivery_date='2024-06-20', status='completed')
        response = self.client.post(f'/api/purchase_orders/{purchase_order.id}/acknowledge/', {'acknowledgment_date': '2024-06-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
