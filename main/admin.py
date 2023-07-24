from django.contrib import admin
from django.utils.safestring import mark_safe

from main.models import OptionType, OptionPrice, CakeUser, CategoryCake, Cake, Order


class OptionPriceInline(admin.TabularInline):
    model = OptionPrice
    extra = 0


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    inlines = [
        OptionPriceInline
    ]

@admin.register(CakeUser)
class CakeUserAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryCake)
class CategoryCakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.img.url}" style="max-height: 200px;">')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['client']