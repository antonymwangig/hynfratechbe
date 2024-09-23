from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.serializers import LoginSerializer, SignupSerializer, UserSerializer
import requests

from users.verify_counsellor import verify


User = get_user_model()

GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

class UserToken():
    def generate_tokens_for_user(self,user):
        """
        Generate access and refresh tokens for the given user
        """
        serializer = TokenObtainPairSerializer()
        token_data = serializer.get_token(user)
        access_token = token_data.access_token
        refresh_token = token_data
        return access_token, refresh_token


userToken=UserToken()



class SignupAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        
        serializer = SignupSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.error_messages})
        user =User.objects.create(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['email'].split(" ")[0],
            last_name=serializer.validated_data['email'].split(" ")[0]            
            )
        user.set_password(serializer.validated_data['password'])
        user.save()
        access_token, refresh_token = userToken.generate_tokens_for_user(user)
        response_data = {
            'user': UserSerializer(user).data,
            'access_token': str(access_token),
            'refresh_token': str(refresh_token)
        }
        return Response(response_data ,status=status.HTTP_201_CREATED)
    
    

class UserLoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        
        print("here")
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'blank email or password'})
        user =User.objects.get(email=serializer.validated_data['email'])
        if not user.check_password(serializer.validated_data['password']):
            return Response({'error': 'Incorrect email or password'})
        access_token, refresh_token = userToken.generate_tokens_for_user(user)
        response_data = {
            'user': UserSerializer(user).data,
            'access_token': str(access_token),
            'refresh_token': str(refresh_token)
        }
        return Response(response_data,status=status.HTTP_200_OK)

class GoogleLoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        user_data = self.google_get_user_info(access_token=request.data["access_token"])

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = userToken.generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)
        except User.DoesNotExist:
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = User.objects.create(
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                registration_method='google',
                phone=''
            )
            access_token, refresh_token = userToken.generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)

            

         
    def google_get_user_info(self, access_token:  str):
        response = requests.get(
            GOOGLE_USER_INFO_URL,
            params={'access_token': access_token}
        )                   
        print(response.json())
        if not response.ok:
            raise ValidationError('Failed to obtain user info from Google.')

        return response.json()
    
    
verify("antonymwangig@gmail.com")

        