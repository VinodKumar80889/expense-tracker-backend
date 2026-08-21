from django.contrib import admin
from .models import Expense
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display=("id","date","category","amount","description")
    search_fields=("category","description")
    list_filter=("category","date")
