from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import RecordSerializer, UrlSerializer
from .models import Record, Url
from users.models import User
from django.utils import timezone
from datetime import timedelta
from .utils import *
from django.conf import settings

class RecordView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가게부 전체 리스트
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        record = Record.objects.filter(user=user).order_by("-created_at")
        serializer = RecordSerializer(record, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 가게부 작성
    @swagger_auto_schema(
        request_body=RecordSerializer,
        operation_summary="가게부 작성",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailRecordView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가게부 상세보기
    def get(self, request, user_id, record_id):
        record = get_object_or_404(Record, user=user_id, id=record_id)
        serializer = RecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 가게부 수정
    @swagger_auto_schema(
        request_body=RecordSerializer,
        operation_summary="가게부 수정",
        responses={200: "성공", 400: "인풋값 에러", 401: "인증 에러", 500: "서버 에러"},
    )
    def put(self, request, user_id, record_id):
        record = get_object_or_404(Record, user=user_id, id=record_id)
        serializer = RecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 가게부 삭제
    @swagger_auto_schema(
        operation_summary="가게부 삭제",
        responses={200: "성공", 401: "인증 에러", 403: "접근 권한 없음", 404: "내용 없음", 500: "서버 에러"},
    )    
    def delete(self, request, user_id, record_id):
        record = get_object_or_404(Record, user=user_id, id=record_id)
        if user_id == request.user.id:
            record.delete()
            return Response({"message": "가게부 삭제완료!"}, status=status.HTTP_200_OK)
        return Response({"error": "작성자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

class RecordCopyView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가게부 복제
    @swagger_auto_schema(
        operation_summary="가게부 복제",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    )    
    def post(self, request, user_id, record_id):
        record = get_object_or_404(Record, user=user_id, id=record_id)
        record.id = None
        serializer = RecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UrlShareView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가게부 공유 리스트
    def get(self, request, record_id):
        record = get_object_or_404(Record, id=record_id)
        url = Url.objects.filter(record=record).order_by("-id")
        serializer = UrlSerializer(url, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 가게부 공유
    @swagger_auto_schema(
        operation_summary="가게부 공유",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    ) 
    def post(self, request, record_id):
        record = get_object_or_404(Record, id=record_id)
        temp_url = convert()
        short_link = settings.SITE_URL + temp_url
        share = Url.objects.create(
            record=record, 
            end_date=timezone.now() + timedelta(minutes=3), 
            link=f"http://127.0.0.1:8000/account/share/{id}",
            short_link=short_link
            )
        return Response({"message": "저장완료", "url":share.short_link}, status=status.HTTP_200_OK)
    
    # 가게부 공유 일괄 삭제
    @swagger_auto_schema(
        operation_summary="가게부 공유 일괄 삭제",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    ) 
    def delete(self, request, record_id):
        record = get_object_or_404(Record, id=record_id)
        url = Url.objects.filter(record=record.id)
        url.delete()
        return Response({"message":"공유 일괄 삭제 완료"}, status=status.HTTP_200_OK)


class UrlValidView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가게부 공유 유효기간 체크
    def get(self, request, url_id):
        link = get_object_or_404(Url, id=url_id)
        if link.end_date > timezone.now():
            record = Record.objects.get(id=link.record.id)
            serializer = UrlSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "유효기간이 지났습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    # 가게부 공유 삭제
    @swagger_auto_schema(
        operation_summary="가게부 공유 삭제",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    ) 
    def delete(self, request, url_id):
        user = request.user.id
        link = get_object_or_404(Url, id=url_id)
        record = get_object_or_404(Record, id=link.record.id)
        if user == record.user.id:
            link.delete()
            return Response({"message": "공유 삭제"}, status=status.HTTP_200_OK)
        
        return Response({"error": "공유자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
