from django.db import models

class TimestampZone(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Record(TimestampZone):
    user = models.ForeignKey("users.user", on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=0)
    choices = [
        ("income", "수입"),
        ("expense", "지출"),
    ]
    settlement_method = [
        ("cash", "현금"),
        ("transfer", "계좌이체"),
        ("card", "카드"),
    ]
    income_expense = models.CharField(
        choices=choices, null=False, default=choices[0][0], max_length=20
    )
    method = models.CharField(
        choices=settlement_method, null=False, default=settlement_method[0][0], max_length=20
    )
    memo = models.CharField(max_length=300, null=True, blank=True)
    