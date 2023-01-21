from django.contrib import admin
from .models import Record, Url

@admin.register(Record)
class Record(admin.ModelAdmin):
    list_display = ('income_expense', 'method', 'memo')
    fields = (
        'user',
        'amount',
        'income_expense',
        'method',
        'memo',
    )
    
@admin.register(Url)
class Url(admin.ModelAdmin):
    list_display = ('end_date', 'link', 'short_link')
    fields = (
        'record',
        'end_date',
        'link',
        'short_link',
    )