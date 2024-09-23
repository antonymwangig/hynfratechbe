from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status



class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('users.urls')),
    ]

    def test_user_create(self):
        dummy_user={"full_name":"xx xxx","email":"xxx@gmail.com","password":"xxxxxx"}
        url = reverse('sign-up')
        response = self.client.post(url,data=dummy_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)
        
    def test_user_login(self):
        dummy_user={"full_name":"xx xxx","email":"xxx@gmail.com","password":"xxxxxx"}
        url = reverse('sign-up')
        response = self.client.post(url,data=dummy_user, format='json')        
        url = reverse('login')
        response = self.client.post(url,data={"email":dummy_user["email"],"password":dummy_user["password"]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
