from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )
from users import views

urlpatterns = [
    path('', views.UserView.as_view(), name="user_view"),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('logout/', views.LogoutView.as_view(), name="logout_view"),
    path('activate/<str:uidb64>/<str:token>/', views.UserActivate.as_view(), name='activate'),

]