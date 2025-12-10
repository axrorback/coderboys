from django.shortcuts import render
from django.contrib.auth import login , authenticate , logout
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not password or not username:
            return Response({
                'status':False,
                'status_code':status.HTTP_400_BAD_REQUEST,
                'message':"username va parol bo'sh bo'lishi mumkin emas",
                'timestamp':datetime.now(),
            }
            )

        if user is None:
            return Response({
                'status':False,
                'status_code':status.HTTP_401_UNAUTHORIZED,
                'message':"Username yoki Parol xato iltimos tekshirib qaytadan urinib ko'ring",
                'timestamp':datetime.now()
            })
        if not user.is_active:
            return Response({
                'status':False,
                'status_code':status.HTTP_403_FORBIDDEN,
                'message':f"Hurmatli {username} sizning akkauntingiz faol emas uni sizga tegishli Email yordamida faollashtiring",
                'timestamp':datetime.now()
            })

        refresh = RefreshToken.for_user(user)
        return Response({
                'status':True,
                'status_code':status.HTTP_200_OK,
                'message':'Login amalga oshirildi',
                'access':str(refresh.access_token),
                'timestamp':datetime.now()
            })



