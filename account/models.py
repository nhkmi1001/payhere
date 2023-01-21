from django.db import models

class TimestampZone(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Record(TimestampZone):
    user = models.ForeignKey("users.user", on_delete=models.CASCADE)
    amount = models.IntegerField("금액", null=False, default=0)
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
        "수입지출", choices=choices, null=False, default=choices[0][0], max_length=20
    )
    method = models.CharField(
        "결제방법", choices=settlement_method, null=False, default=settlement_method[0][0], max_length=20
    )
    memo = models.CharField("메모", max_length=300, null=True, blank=True)

class Url(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    end_date = models.DateTimeField("유효기간", null=False)
    link = models.URLField("기존링크", max_length=200, null=False)
    short_link = models.URLField("단축링크", default="", null=False)