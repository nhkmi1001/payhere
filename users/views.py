from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from django.contrib.auth import logout

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import redirect
from users.token import account_activation_token
import traceback

class UserView(APIView):
    permission_classes = [AllowAny] 
    
    # 회원가입
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_summary="회원가입",
        responses={201: "성공", 400: "인풋값 에러", 404: "찾을 수 없음", 500: "서버 에러"},
        )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        operation_summary="회원정보 수정",
        responses={200: "성공", 400: "인풋값 에러", 401: "인증 오류", 404: "찾을 수 없음", 500: "서버 에러"},
        )    
    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원 수정 완료."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        user.email = "*"
        user.password = "*"
        user.save()
        return Response({"message": "회원 탈퇴 완료"}, status=status.HTTP_200_OK)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
# 로그아웃
class LogoutView(APIView):
    parser_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
    
class UserActivate(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect("http://127.0.0.1:5500/templates/email-done.html")
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())
