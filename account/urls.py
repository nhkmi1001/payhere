from django.urls import path

from . import views

urlpatterns = [
    path('<int:user_id>/', views.RecordView.as_view(), name="record_view"),
    path('<int:user_id>/<int:record_id>/', views.DetailRecordView.as_view(), name="detail_record_view"),
       
]
