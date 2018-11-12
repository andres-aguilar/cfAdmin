from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import Client, SocialNetwork


class ClientAdmin(admin.ModelAdmin):
    exclude = ('user',)


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False


class SocialNetworkInline(admin.StackedInline):
    model = SocialNetwork
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [ClientInline, SocialNetworkInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)