from django.contrib import admin
from main.models import Category, Wallet, IncomeExpense


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_en', 'name_ru', 'is_income',]
    readonly_fields = ['is_income',]
    list_filter = ['is_income',]
    search_fields = ['name_uz', 'name_en', 'name_ru',]


class WalletAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_en', 'name_ru', 'balance',]


class IncomeExpenseAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'summa', 'wallet', 'category', 'is_income',]
    list_filter = ['date_time', 'wallet', 'category', ]
    search_fields = ['wallet__name', 'category__name', ]
    ordering = ['date_time',]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(IncomeExpense, IncomeExpenseAdmin)
