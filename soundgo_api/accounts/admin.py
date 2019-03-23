from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAccountAdmin
from django.contrib.auth.models import Group

from .forms import UserAccountAdminCreationForm, UserAccountAdminChangeForm

from .models import Actor, Language, SoundGoConfig

UserAccount = get_user_model()


class ActorInline(admin.TabularInline):

    model = Actor
    can_delete = False
    verbose_name_plural = "ACTOR"
    min_num = 1

    fields = ("photo", "email", "minutes", "language")


class UserAccountAdmin(BaseUserAccountAdmin):

    form = UserAccountAdminChangeForm
    add_form = UserAccountAdminCreationForm

    inlines = (ActorInline,)

    list_display = ('nickname', 'active', 'admin')

    list_filter = ('active', 'admin')

    fieldsets = (
        ("ACCOUNT INFORMATION", {'fields': ('nickname', 'password')}),
        ("PERMISSIONS", {'fields': ('active', 'admin')}),
    )

    add_fieldsets = (
        ("ACCOUNT INFORMATION", {
            'classes': ('wide',),
            'fields': ('nickname', 'password1', 'password2')
        }),
        ("PERMISSIONS", {
            'classes': ('wide',),
            'fields': ('active', 'admin')
        }),
    )

    # Fields used to search in the users list
    search_fields = ('nickname',)

    # Fields used to order in the users list
    ordering = ('nickname',)

    # Empty horizontal filter (we do not use it)
    filter_horizontal = ()


class LanguageAdmin(admin.ModelAdmin):

    actions = []

    def has_delete_permission(self, request, obj=None):
        return False


class ConfigurationAdmin(admin.ModelAdmin):

    actions = []

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.unregister(Group)
admin.site.register(Language, LanguageAdmin)
admin.site.register(SoundGoConfig, ConfigurationAdmin)
