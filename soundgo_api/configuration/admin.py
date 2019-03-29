from django.contrib import admin

from .models import Configuration


class ConfigurationAdmin(admin.ModelAdmin):

    actions = []

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Configuration, ConfigurationAdmin)
