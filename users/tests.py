from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User

class UserSignupTestCase(APITestCase):
    # 회원가입 성공
    def test_signup_success(self):
        user_data = {
            "email": "test@test.com",
            "password": "Test1234!",
            "passwordcheck": "Test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 201)
    
    # 회원가입 실패(이메일 공란)    
    def test_signup_email_blank_fail(self):
        user_data = {
            "email": "",
            "password": "Test1234!",
            "passwordcheck": "Test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
        
    # 회원가입 실패(이메일 형식)
    def test_signup_email_invalid_fail(self):
        user_data = {
            "email": "test",
            "password": "Test1234!",
            "passwordcheck": "Test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(이메일 중복)
    def test_signup_email_unique_fail(self):
        User.objects.create_user("test@test.com", "Test1234!", "Test1234!")
        user_data = {
            "email": "test@test.com",
            "password": "Test1234!",
            "passwordcheck": "Test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(비밀번호 공란)
    def test_signup_password_blank_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "",
            "passwordcheck": "Test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(비밀번호 체크 공란)
    def test_signup_password_blank_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "Test1234!",
            "passwordcheck": ""
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(비밀번호 != 비밀번호 체크)
    def test_signup_password_equal_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "Test1234!",
            "passwordcheck": "Test12345!!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(비밀번호 형식(길이))
    def test_signup_password_invalid_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "T12",
            "passwordcheck": "T12"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
        
    # 회원가입 실패(비밀번호 형식(대소문자))
    def test_signup_password_invalid_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234!",
            "passwordcheck": "test1234!"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)
        
    # 회원가입 실패(비밀번호 형식(특수문자))
    def test_signup_password_invalid_fail(self):
        user_data = {
            "email": "test@test.com",
            "password": "Test12345",
            "passwordcheck": "Test12345"
        }
        response = self.client.post(reverse("user_view"), user_data)
        self.assertEqual(response.status_code, 400)

class UserUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "password": "Test1234!"}
        self.user1 = User.objects.create_user("test@test.com", "Test1234!")
        self.user2 = User.objects.create_user("test1@test.com", "Test1234!")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair_view"), self.user_data).data["access"]
    
    # 회원정보 수정 성공
    def test_user_update_success(self):
        response = self.client.put(
            path = reverse("user_view"),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            data = {"email": "test11@test.com"}
        )
        self.assertEqual(response.status_code, 200)
    
