from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status



class ServicePlanTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('users.urls')),
        path('api/', include('plans.urls')),
    ]

        
    def test_service_plans(self):
        dummy_user={"full_name":"xx xxx","email":"xxx@gmail.com","password":"xxxxxx"}
        url = reverse('sign-up')
        response = self.client.post(url,data=dummy_user, format='json')        
        url = reverse('login')
        response = self.client.post(url,data={"email":dummy_user["email"],"password":dummy_user["password"]}, format='json')
        response = self.client.get("/api/service-plans/",headers={"Authorization": f"Bearer {response.data['access_token']}"})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
