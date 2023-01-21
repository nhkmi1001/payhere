from rest_framework import serializers
from .models import Record, Url

class RecordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Record
        fields = ("amount", "income_expense", "method", "memo", )
        
class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__"
        