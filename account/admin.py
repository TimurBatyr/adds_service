from django.contrib import admin

from account.models import UserProfile


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = [
#         'name',
#         'last_name',
#         'is_active',
#         'email',
#     ]

admin.site.register(UserProfile)