from django.urls import path

from . import views

urlpatterns = [
    path('<int:user_id>/', views.RecordView.as_view(), name="record_view"),
    path('<int:user_id>/<int:record_id>/', views.DetailRecordView.as_view(), name="detail_record_view"),
    path('<int:user_id>/<int:record_id>/copy/', views.RecordCopyView.as_view(), name="record_copy_view"),
    path('<int:record_id>/share/', views.UrlShareView.as_view(), name="url_share_view"),
    path('share/<int:url_id>/', views.UrlValidView.as_view(), name="url_valid_view"),
]
