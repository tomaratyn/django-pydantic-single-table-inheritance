from django.contrib import admin

from onetable_with_pydantic.models import BaseIntegration, CoreModel, IntegrationB, IntegrationA


class IntegrationBAdmin(admin.ModelAdmin):
    model = IntegrationB
    def get_queryset(self, request):
        """
        Override the queryset to use the custom manager.
        """
        return self.model.objects.get_queryset()


admin.site.register(IntegrationB, IntegrationBAdmin)


class IntegrationAAdmin(admin.ModelAdmin):
    model = IntegrationA
    def get_queryset(self, request):
        """
        Override the queryset to use the custom manager.
        """
        return self.model.objects.get_queryset()


admin.site.register(IntegrationA, IntegrationAAdmin)

admin.site.register(CoreModel)
