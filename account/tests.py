from rest_framework.test import APITestCase
from django.urls import reverse
from account.models import Record, Url
from users.models import User

class RecordViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.user = User.objects.create_user("test@test.com", "Test1234!")
        cls.record_data = {"amount": "100", "income_expense": "income", "method": "cash", "memo": "테스트"}
        cls.record_data1 = {"amount": "100", "income_expense": "", "method": "cash", "memo": "테스트"}
        cls.record_data2 = {"amount": "100", "income_expense": "income", "method": "", "memo": "테스트"}

        cls.record = Record.objects.create(
            user = cls.user,
            amount = "100",
            income_expense = "income",
            method = "cash",
            memo = "테스트"
        )
    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair_view"), self.user_data).data["access"]
    
    # 가게부 조회 성공
    def test_record_list_success(self):
        response = self.client.get(
            path = reverse("record_view", kwargs={"user_id" : 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
        )    
        self.assertEqual(response.status_code, 200)

    # 가게부 작성 성공
    def test_record_post_success(self):
        response = self.client.post(
            path = reverse("record_view", kwargs={"user_id" : self.user.id}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            data = self.record_data,
        )
        self.assertEqual(response.status_code, 200)
    
    # 비로그인 유저 가게부 작성
    def test_record_post_not_logged_fail(self):
        response = self.client.post(
            path = reverse("record_view", kwargs={"user_id" : 2}),
            data = self.record_data,
        )
        self.assertEqual(response.status_code, 401)
    
    # 가게부 작성 실패(수입지출 선택x)
    def test_record_post_blank_settlement_fail(self):
        response = self.client.post(
            path = reverse("record_view", kwargs={"user_id" : 2}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            data = self.record_data1,
        )
        self.assertEqual(response.status_code, 404)

class DetailRecordTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {"email": "test1@test.com", "password": "Test1234!"}
        cls.user2_data = {"email": "test2@test.com", "password": "Test1234!"}
        cls.user3_data = {"email": "test3@test.com", "password": "Test1234!"}
        cls.user1 = User.objects.create_user("test1@test.com", "Test1234!")
        cls.user2 = User.objects.create_user("test2@test.com", "Test1234!")
        cls.user3 = User.objects.create_user("test3@test.com", "Test1234!")
        cls.record1_data = {"amount": "100", "income_expense": "income", "method": "cash", "memo": "테스트"}
        cls.record2_data = {"amount": "200", "income_expense": "expense", "method": "cash", "memo": "테스트"}

        cls.record = Record.objects.create(
            user = cls.user1,
            amount = "100",
            income_expense = "income",
            method = "cash",
            memo = "테스트"
        )
    def setUp(self):
        self.access_token_1 = self.client.post(reverse("token_obtain_pair_view"), self.user1_data).data["access"]
        self.access_token_2 = self.client.post(reverse("token_obtain_pair_view"), self.user2_data).data["access"]
        self.access_token_3 = self.client.post(reverse("token_obtain_pair_view"), self.user3_data).data["access"]

    # 가게부 상세보기 성공
    def test_detail_record_success(self):
        response = self.client.get(
            path = reverse("detail_record_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}",
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 수정 성공
    def test_detail_record_put_success(self):
        response = self.client.put(
            path = reverse("detail_record_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}",
            data = self.record2_data
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 수정 실패(작성자 아님)
    def test_detail_record_put_user_fail(self):
        response = self.client.put(
            path = reverse("detail_record_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}",
            data = self.record2_data
        )
        self.assertEqual(response.status_code, 401)

    # 가게부 삭제 성공
    def test_detail_record_delete_success(self):
        response = self.client.delete(
            path = reverse("detail_record_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
        
    # 가게부 삭제 실패(작성자 아님)
    def test_detail_record_delete_user_fail(self):
        response = self.client.delete(
            path = reverse("detail_record_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}"
        )
        self.assertEqual(response.status_code, 401)

class RecordCopyTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {"email": "test1@test.com", "password": "Test1234!"}
        cls.user2_data = {"email": "test2@test.com", "password": "Test1234!"}
        cls.user1 = User.objects.create_user("test1@test.com", "Test1234!")
        cls.user2 = User.objects.create_user("test2@test.com", "Test1234!")
        cls.record1_data = {"amount": "100", "income_expense": "income", "method": "cash", "memo": "테스트"}
        cls.record = Record.objects.create(
            user = cls.user1,
            amount = "100",
            income_expense = "income",
            method = "cash",
            memo = "테스트"
        )
    def setUp(self):
        self.access_token_1 = self.client.post(reverse("token_obtain_pair_view"), self.user1_data).data["access"]
        self.access_token_2 = self.client.post(reverse("token_obtain_pair_view"), self.user2_data).data["access"]

    # 가게부 복제 성공
    def test_record_copy_success(self):
        response = self.client.post(
            path = reverse("record_copy_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
       
    # 가게부 복제 실패    
    def test_record_copy_user_fail(self):
        response = self.client.post(
            path = reverse("record_copy_view", kwargs={"user_id": 1, "record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}"
        )
        self.assertEqual(response.status_code, 401)
    
class UrlShareTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {"email": "test1@test.com", "password": "Test1234!"}
        cls.user2_data = {"email": "test2@test.com", "password": "Test1234!"}
        cls.user1 = User.objects.create_user("test1@test.com", "Test1234!")
        cls.user2 = User.objects.create_user("test2@test.com", "Test1234!")
        cls.record1_data = {"amount": "100", "income_expense": "income", "method": "cash", "memo": "테스트"}
        cls.record = Record.objects.create(
            user = cls.user1,
            amount = "100",
            income_expense = "income",
            method = "cash",
            memo = "테스트"
        )
    def setUp(self):
        self.access_token_1 = self.client.post(reverse("token_obtain_pair_view"), self.user1_data).data["access"]
        self.access_token_2 = self.client.post(reverse("token_obtain_pair_view"), self.user2_data).data["access"]

    # 가게부 공유 리스트 성공
    def test_url_share_success(self):
        response = self.client.post(
            path = reverse("url_share_view", kwargs={"record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 공유 성공
    def test_url_share_post_success(self):
        response = self.client.post(
            path = reverse("url_share_view", kwargs={"record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 공유 일괄 삭제
    def test_url_share_delete_bulk_success(self):
        response = self.client.delete(
            path = reverse("url_share_view", kwargs={"record_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)

class UrlValidTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {"email": "test1@test.com", "password": "Test1234!"}
        cls.user2_data = {"email": "test2@test.com", "password": "Test1234!"}
        cls.user1 = User.objects.create_user("test1@test.com", "Test1234!")
        cls.user2 = User.objects.create_user("test2@test.com", "Test1234!")
        cls.record1_data = {"amount": "100", "income_expense": "income", "method": "cash", "memo": "테스트"}
        cls.record = Record.objects.create(
            user = cls.user1,
            amount = "100",
            income_expense = "income",
            method = "cash",
            memo = "테스트"
        )
        cls.url1 = Url.objects.create(
            record = cls.record,
            end_date = "2023-01-21 15:37:45.800648+00:00",
            link = "http://127.0.0.1:8000/",
            short_link = "http://127.0.0.1:8000/",
        )
    def setUp(self):
        self.access_token_1 = self.client.post(reverse("token_obtain_pair_view"), self.user1_data).data["access"]
        self.access_token_2 = self.client.post(reverse("token_obtain_pair_view"), self.user2_data).data["access"]

    # 가게부 공유 유효시간 체크 성공
    def test_url_valid_success(self):
        response = self.client.get(
            path = reverse("url_valid_view", kwargs={"url_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 공유 삭제 성공
    def test_url_share_delete_success(self):
        response = self.client.delete(
            path = reverse("url_valid_view", kwargs={"url_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}"
        )
        self.assertEqual(response.status_code, 200)
    
    # 가게부 공유 삭제 실패(권한 없음)
    def test_url_share_delete_user_fail(self):
        response = self.client.delete(
            path = reverse("url_valid_view", kwargs={"url_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}"
        )
        self.assertEqual(response.status_code, 401)