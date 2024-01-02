from django.contrib import admin

from .models import Block, GroupBlock, PrivateBlock
# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    list_display = ['name', 'online_users_count']
    list_filter = ['name']
    search_fields = ['name']

    def online_users_count(self, obj):
        return obj.online_users()
    online_users_count.short_description = 'Online Users'


admin.site.register(Block, BlockAdmin)


class GroupBlockAdmin(admin.ModelAdmin):
    list_display = ['user', 'block', 'content', 'pub_date']
    list_filter = ['user', 'block', 'content', 'pub_date']
    search_fields = ['user', 'block', 'content']


admin.site.register(GroupBlock, GroupBlockAdmin)


class PrivateBlockAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'block_thread', 'pub_date']
    list_filter = ['user', 'message', 'block_thread', 'pub_date']
    search_fields = ['user', 'message', 'block_thread']


admin.site.register(PrivateBlock, PrivateBlockAdmin)
