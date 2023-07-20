from django.contrib import admin
from main.models import OptionType, OptionPrice, CakeUser, CategoryCake, Cake, Order

admin.site.register(CakeUser)
admin.site.register(CategoryCake)
admin.site.register(Cake)
admin.site.register(Order)

class OptionPriceInline(admin.TabularInline):
    model = OptionPrice
    extra = 0


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    inlines = [
        OptionPriceInline
    ]
