# Generated by Django 4.1.5 on 2023-01-19 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.IntegerField(default=0)),
                (
                    "income_expense",
                    models.CharField(
                        choices=[("income", "수입"), ("expense", "지출")],
                        default="income",
                        max_length=20,
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[("cash", "현금"), ("transfer", "계좌이체"), ("card", "카드")],
                        default="cash",
                        max_length=20,
                    ),
                ),
                ("memo", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]