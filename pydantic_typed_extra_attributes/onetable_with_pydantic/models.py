from dataclasses import asdict
from functools import cached_property
from typing import Dict

from django.db import models
from model_utils.managers import InheritanceManager
from model_utils.models import TimeFramedModel
from pydantic import BaseModel, ValidationError

from onetable_with_pydantic.exceptions import BadIntegrationExtraException


class CoreModel(models.Model):
    """
    This is a core model has to use integrations.
    """
    name = models.CharField(max_length=255)
    integration = models.ForeignKey('BaseIntegration', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.__class__.__name__}"

    @cached_property
    def concrete_integration(self):
        """
        Return the concrete integration instance.
        """
        return self.integration.get_implementation()


class IntegrationManager(InheritanceManager):
    """
    Custom manager for integrations
    """

    def get_queryset(self):
        """
        Return the queryset for the model.
        """
        if hasattr(self.model, 'INTEGRATION_ID'):
            return self.get_unfiltered_queryset().filter(type=self.model.INTEGRATION_ID)
        return self.get_unfiltered_queryset()

    def get_unfiltered_queryset(self):
        return super().get_queryset().select_subclasses()

    def create_from_data(self, data):
        try:
            integration_a_extras = self.model.SCHEMA(**asdict(data))
        except ValidationError as e:
            raise ValueError(f"Invalid data for Integration A: {e}") from e
        return self.create(
            name=data.name,
            type=self.model.INTEGRATION_ID,
            is_active=True,
            start=data.start,
            end=data.end,
            extra=integration_a_extras.dict(),
        )


class BaseIntegration(TimeFramedModel):
    """
    Base model for integrations with common fields.
    """

    class Integrations(models.TextChoices):
        INTEGRATION_A = 'Integration A'
        INTEGRATION_B = 'Integration B'

    SUBCLASS_INTEGRATIONS: Dict[Integrations, str] = {
        Integrations.INTEGRATION_A: 'IntegrationA',
        Integrations.INTEGRATION_B: 'IntegrationB',
    }

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    extra = models.JSONField(default=dict)
    type = models.TextField(
        choices=Integrations.choices,
    )

    objects = IntegrationManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.SCHEMA.model_validate(self.extra)
        except ValidationError as e:
            raise BadIntegrationExtraException('Bad extra') from e
        else:
            return super().save(*args, **kwargs)

    def parse_extra(self) -> BaseModel:
        """
        Parse the extra field into a Pydantic model.
        """
        if not hasattr(self, '_parsed_extra') or self._parsed_extra is None:
            try:
                self._parsed_extra = self.SCHEMA.model_validate(self.extra)
            except ValidationError as e:
                raise BadIntegrationExtraException(f"Invalid extra data: {e}") from e

        return self._parsed_extra

    def get_implementation(self):
        """
        Get the implementation of the integration.
        """
        integration_type = self.Integrations(self.type)
        subclass_name = self.SUBCLASS_INTEGRATIONS[integration_type]
        subclass = globals()[subclass_name]
        field_names = (f.name for f in self._meta.get_fields(include_parents=True))
        subclass_args = {
            name: getattr(self, name) for name in field_names if hasattr(self, name)
        }
        return subclass(**subclass_args)


class IntegrationAExtraSchema(BaseModel):
    """
    Extra schema for Integration A.
    """
    custom_prop_a: str


class IntegrationA(BaseIntegration):
    """
    Model for Integration A.
    """
    SCHEMA = IntegrationAExtraSchema
    INTEGRATION_ID = BaseIntegration.Integrations.INTEGRATION_A

    class Meta:
        proxy = True


class IntegrationBExtraSchema(BaseModel):
    """
    Extra schema for Integration A.
    """
    custom_prop_b: str


class IntegrationB(BaseIntegration):
    """
    Model for Integration A.
    """
    SCHEMA = IntegrationBExtraSchema
    INTEGRATION_ID = BaseIntegration.Integrations.INTEGRATION_B

    class Meta:
        proxy = True
