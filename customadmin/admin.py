from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render

from chat.models import Block, GroupBlock, PrivateBlock
# Register your models here.


class CustomAdminArea(admin.AdminSite):
    site_header = 'Candlechat Admin'
    login_template = 'customadmin/login.html'
    index_template = 'customadmin/index.html'  # Set the custom index template path

    def index(self, request, extra_context=None):
        context = {
            **self.each_context(request),
            **(extra_context or {}),
        }

        return render(request, self.index_template, context)

custom_admin_site = CustomAdminArea(name='CustomAdmin')


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_superuser']
    list_filter = ['username', 'first_name', 'last_name', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name']


class BlockAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    list_display = ['name', 'online_users_count']
    list_filter = ['name']
    search_fields = ['name']

    def online_users_count(self, obj):
        return obj.online_users()
    online_users_count.short_description = 'Online Users'


# resgiter models to custom admin
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Block, BlockAdmin)