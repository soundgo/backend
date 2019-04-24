from django.contrib import admin

from .models import Site


class SiteAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):

        self.readonly_fields = ('longitude', 'latitude', 'actor')

        return super(SiteAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Site, SiteAdmin)
