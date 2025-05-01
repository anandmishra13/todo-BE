import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from mongoengine.errors import NotUniqueError
from .models import User
from .serializers import UserSerializer
import hashlib
import json


class Register(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects(username=username).first():
            return JsonResponse(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        hashed_password = make_password(password)

        user = User(username=username, password=hashed_password)
        user.save()

        return JsonResponse(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse(
                {"error": "username and password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, user.password):
            return JsonResponse(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        payload = {
            'id': str(user.id),
            'username': str(user.username)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return JsonResponse({
            "status": "success",
            "id": str(user.id),
            "username": user.username,
            "token": token
        }, status=status.HTTP_200_OK)



# @csrf_exempt
# def hash_password(password):
#     return hashlib.sha1(password.encode('utf-8')).hexdigest()

# @csrf_exempt
# def register_user(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#
#         username = data.get('username')
#         password = data.get('password')
#
#         if not username or not password:
#             return JsonResponse({
#                 "error": "Username and password is required"
#             }, status=400)
#
#         try:
#             user = User(
#                 username=username,
#                 password=hash_password(password)
#             )
#             user.save()
#             return JsonResponse({
#                 "message": "User Registered successfully"
#             })
#         except NotUniqueError:
#             return JsonResponse({
#                 "error": "Username already Exist"
#             }, status=400)
#
# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#
#         username = data.get('username')
#         password = hash_password(data.get('password'))
#
#         user = User.objects(username=username, password=password).first()
#
#         if user:
#             return JsonResponse({
#                 'message': "Login successful"
#             }, status=201)
#         else:
#             return JsonResponse({
#                 'error': "Invalid Username or password "
#             },status=401)

