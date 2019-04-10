from django.contrib import admin

from .models import Site
from accounts.models import Actor


class SiteAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'actor':

            kwargs['initial'] = Actor.objects.filter(user_account=request.user).all()[0]
            kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        self.readonly_fields = ('longitude', 'latitude', 'actor')

        return super(SiteAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Site, SiteAdmin)
