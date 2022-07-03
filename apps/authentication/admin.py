# Django imports
from django.contrib import admin

# external imports
from rest_framework_simplejwt import token_blacklist
from rest_framework_simplejwt.token_blacklist.admin import (
    OutstandingTokenAdmin,
)

# app imports
from .models import LoginDevice

admin.site.register(LoginDevice)


class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True  # or whatever logic you want


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(
    token_blacklist.models.OutstandingToken, OutstandingTokenAdmin
)
# http://127.0.0.1/api/v1/self-service/auth/email/verify?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWN0aXZhdGlvbiIsImV4cCI6MTY1NjIzNjIwNSwiaWF0IjoxNjU2MjM1NjA1LCJqdGkiOiI3MTY2ODY4MGE5NzU0YTBkODA3NjE5ODU0YjRjNDIwMyIsInVzZXJfaWQiOjV9.4xiHpwvqMVd4n8Rup_MZADzFBBvUs4mdNSqls1xfOg8
# http://127.0.0.1:8000/admin/sites/site/2/change/