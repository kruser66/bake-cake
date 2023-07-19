from django.contrib import admin
from main.models import OptionType, OptionPrice


class OptionPriceInline(admin.TabularInline):
    model = OptionPrice
    extra = 0


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    inlines = [
        OptionPriceInline
    ]