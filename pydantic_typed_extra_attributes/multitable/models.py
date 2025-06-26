from django.db import models
from model_utils.models import TimeFramedModel

class CoreModel(models.Model):
    """
    This is a core model that works with many integrations.
    """
    integration = models.ForeignKey('BaseIntegration', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class BaseIntegration(TimeFramedModel):
    """
    Base model for integrations with common fields.
    """
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class IntegrationA(BaseIntegration):
    """
    Model for Integration A.
    """
    custom_prop_a = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Integration A"
        verbose_name_plural = "Integrations A"

class IntegrationB(BaseIntegration):
    """
    Model for Integration B.
    """
    custom_prop_b = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Integration B"
        verbose_name_plural = "Integrations B"

