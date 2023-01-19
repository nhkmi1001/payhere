from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import RecordSerializer
from .models import Record
from users.models import User
from .utils import make_dict_to_url, make_url_to_dict, check_valid_log_url

class RecordView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가계부 전체 리스트
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if user:
            record = Record.objects.filter(user=user).order_by("-created_at")
            serializer = RecordSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # 가게부 작성
    @swagger_auto_schema(
        request_body=RecordSerializer,
        operation_summary="가게부 작성",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request, user_id):
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
            return Response({"message": "삭제완료!"}, status=status.HTTP_200_OK)
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

# class MakeShortUrl(APIView):
#     def get(self, request, url=None):
#         is_valid_url = check_valid_log_url(url)
#         if not is_valid_url:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         record_url = make_url_to_dict(url)
#         instance = 