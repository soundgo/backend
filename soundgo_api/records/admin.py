from django.contrib import admin

from .models import Audio, Advertisement, Category


class CategoryAdmin(admin.ModelAdmin):

    actions = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Audio)
admin.site.register(Advertisement)
admin.site.register(Category, CategoryAdmin)
