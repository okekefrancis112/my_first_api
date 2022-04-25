from django.urls import reverse, resolve
from django.test import SimpleTestCase
from api.views import CustomerView
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlsTests(SimpleTestCase):
    
    def test_get_customers_is_resolved(self):
        url = reverse('customer')
        self.assertEquals(resolve(url).func.view_class, CustomerView)
        
class CustomerAPIViewTests(APITestCase):
    
    customers_url = reverse('customer')
    
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_get_customers_authenticated(self):
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_customers_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        # print("error... ", a)
        response = self.client.get(self.customers_url)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_customer_authenticated(self):
        data = {
            "title": "Mr",
            "name": "Peter",
            "last_name": "Parker",
            "gender": "M",
            "status": "published"
        }
        response = self.client.post(self.customers_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Peter')
        
    # def test_post_customer_un_authenticated(self):
    #     data = {
    #         "title": "Mr",
    #         "name": "Peter",
    #         "last_name": "Parker",
    #         "gender": "M",
    #         "status": "published"
    #     }
    #     response = self.client.post(self.customers_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['name'], 'Peter ')
        
class CustomerDetailAPIViewTests(APITestCase):
    customers_url = reverse('customer')
    customer_url = reverse('customer-detail', args=[1])
    
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Saving User
        data = {
                "title": "Mr",
                "name": "Chris",
                "last_name": "Deji",
                "gender": "M",
                "status": "published"
            }
        response = self.client.post(self.customers_url, data, format='json')
        
    def test_get_customer_authenticated(self):
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Chris')
        
    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.data['name'], 'Chris')
        
    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    # run put request test

