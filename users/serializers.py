from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms import ValidationError
import re
from users.token import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()
    
# 회원가입 serializer
class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)
    
    class Meta:
        model = User
        fields = ("email", "password", "passwordcheck")
        extra_kwargs = {
            "password":{
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호를 입력해주세요.",
                    "blank": "비밀번호를 입력해주세요."
                }
            },
            "email":{
                "error_messages":{
                    "required": "이메일을 입력해주세요.",
                    "invalid": "이메일 형식을 확인해주세요.",
                    "blank": "이메일을 입력해주세요."
                }
            },
            "passwordcheck":{
                "read_only": True,
            }
        }
    def create(self, validated_data):
        email = validated_data["email"]
        user = User(email=email)
        password = user.password
        user.set_password(password)
        user.is_active = False
        user.save()
        message = render_to_string('user/account_activate_email.html', {
          'user': user,
          'domain': 'localhost:8000',
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Payhere 회원가입 인증 이메일입니다.'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        EmailThread(email).start()
        email.content_subtype = "html"
        return validated_data    
    
    def validate(self, data):
        REGEX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
        email = data.get("email")
        password = data.get("password")
        passwordcheck = data.get("passwordcheck")
        
        # 이메일 형식
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError(detail={"email": "이메일형식이 아닙니다."})
        
        # 비밀번호 형식
        if not re.match(REGEX_PASSWORD, password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상 16자 이하의 길이와 대/소문자, 숫자, 특수문자로 조합해주세요."})
        
        # 비밀번호, 비밀번호 확인 동일 검사
        if password != passwordcheck:
            raise serializers.ValidationError(detail={"password": "비밀번호가 다릅니다. 확인해주세요."})

        # 이메일 존재 여부
        if (User.objects.filter(email=data['email']).exists()):
            raise serializers(detail={"email": "이미 사용중인 이메일입니다."})
        return data
    

    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token


# 회원정보 수정 serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", )
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "이메일을 입력해주세요.",
                    "invalid": "형식을 맞춰주세요.",
                    "blank": "이메일을 입력해주세요."
                }
            }
        }
        def update(self, obj, validated_data):
            obj.email = validated_data.get("email", obj.email)
            obj.save()
            
            return obj
            