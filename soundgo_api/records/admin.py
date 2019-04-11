from django.contrib import admin

from .models import Audio, Advertisement, Category, Like, Report, Reproduction


class AudioAdmin(admin.ModelAdmin):

    list_filter = ('isInappropriate', )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AdvertisementAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):

    actions = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Audio, AudioAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Category, CategoryAdmin)
