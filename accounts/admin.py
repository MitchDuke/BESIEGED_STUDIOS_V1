from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'formatted_address')

    def formatted_address(self, obj):
        return f"{obj.address_line1}, {obj.address_line2}, {obj.town_or_city}, {obj.postcode}"
    formatted_address.short_description = 'Address'
