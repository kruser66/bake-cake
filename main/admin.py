from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from main.models import OptionType, OptionPrice, CakeUser, CategoryCake, Cake, Order


def format_preview_image(image, height='200px'):
    return format_html(
        '<img src="{url}" height="{height}"/>',
        url=image.image.url,
        height=height,
    )

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
    readonly_fields = [format_preview_image]

    # def preview(self, obj):
    #     return mark_safe(f'<img src="{obj.img.url}" style="max-height: 200px;">')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass