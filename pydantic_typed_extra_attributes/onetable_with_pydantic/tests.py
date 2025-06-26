from datetime import datetime, timezone

from django.test import TestCase

from onetable_with_pydantic.api import IntegrationAData, IntegrationBData
from onetable_with_pydantic.models import IntegrationA, BaseIntegration, IntegrationB, \
    CoreModel
from onetable_with_pydantic.exceptions import BadIntegrationExtraException

INTEGRATION_A_DATA = IntegrationAData(
    start=datetime(2023, 1, 1, tzinfo=timezone.utc),
    end=datetime(2024, 12, 31, tzinfo=timezone.utc),
    name="Integration A",
    custom_prop_a="Custom Property A"
)

INTEGRATION_B_DATA = IntegrationBData(
    start=datetime(2023, 1, 1, tzinfo=timezone.utc),
    end=datetime(2024, 12, 31, tzinfo=timezone.utc),
    name="Integration B",
    custom_prop_b="Custom Property B"
)


class TestCreation(TestCase):
    def test_creating_integration_a(self):
        integration_model = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)

        self.assertIsNotNone(integration_model)
        self.assertEqual(integration_model.type, BaseIntegration.Integrations.INTEGRATION_A)


class TestRetrieval(TestCase):

    def test_get_integration_a(self):
        original = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        integration_a = IntegrationA.objects.get(id=original.id)

        extra = integration_a.parse_extra()
        self.assertEqual(extra.custom_prop_a, INTEGRATION_A_DATA.custom_prop_a)


class TestSaving(TestCase):

    def test_saving_integration_a(self):
        integration_model = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        integration_model.name = "Updated Integration A"
        integration_model.save()

    def test_saving_invalid_data(self):
        integration_model = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        integration_model.extra = {"invalid_key": "invalid_value"}
        with self.assertRaises(BadIntegrationExtraException):
            integration_model.save()


class TestWrongDataAndClass(TestCase):
    """
    Test what happens if you try to save integration A with data from integration B.
    """

    def test_creation_with_wrong_data(self):
        with self.assertRaises(ValueError):
            IntegrationA.objects.create_from_data(INTEGRATION_B_DATA)

        with self.assertRaises(ValueError):
            IntegrationB.objects.create_from_data(INTEGRATION_A_DATA)

    def test_cannot_get_wrong_integration(self):
        original = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        with self.assertRaises(IntegrationB.DoesNotExist):
            IntegrationB.objects.get(id=original.id)


class TestCoreDataAndIntegrations(TestCase):
    """
    Test that we can use a core data with integrations
    """

    def setUp(self):
        imodel = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        self.original_core_model = CoreModel.objects.create(
            name="Core Model with Integration A",
            integration=imodel
        )

    def test_make_core_data_with_integration(self):
        retrieved_core_model = CoreModel.objects.get(id=self.original_core_model.id)
        self.assertEqual(retrieved_core_model.concrete_integration.parse_extra().custom_prop_a,
                         INTEGRATION_A_DATA.custom_prop_a)

    def test_can_update_integration(self):
        retrieved_core_model = CoreModel.objects.get(id=self.original_core_model.id)
        retrieved_core_model.concrete_integration.name = "Updated Integration A"
        retrieved_core_model.concrete_integration.save()

        base_instance = BaseIntegration.objects.get_unfiltered_queryset().get(id=retrieved_core_model.concrete_integration.id)
        fresh_integration_instance = (base_instance.get_implementation())
        self.assertEqual(fresh_integration_instance.name, "Updated Integration A")
        self.assertEqual(fresh_integration_instance.parse_extra().custom_prop_a, INTEGRATION_A_DATA.custom_prop_a)


class TestBaseIntegrationGetImplementation(TestCase):
    """
    Test that we can get the implementation of a base integration.
    """

    def setUp(self):
        self.integration_a = IntegrationA.objects.create_from_data(INTEGRATION_A_DATA)
        self.original_core_model = CoreModel.objects.create(
            name="Core Model with Integration A",
            integration=self.integration_a
        )

    def test_get_implementation(self):
        integration = (BaseIntegration
                       .objects
                       .get_unfiltered_queryset()
                       .get(id=self.integration_a.id)
                       .get_implementation())
        self.assertEqual(integration.coremodel_set.count(), 1)
        self.assertEqual(integration.coremodel_set.first().id, self.original_core_model.id)
