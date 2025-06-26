from django.contrib import admin

from multitable.models import IntegrationA, IntegrationB, CoreModel, BaseIntegration

# Register your models here.

admin.site.register(CoreModel)
admin.site.register(BaseIntegration)
admin.site.register(IntegrationA)
admin.site.register(IntegrationB)
