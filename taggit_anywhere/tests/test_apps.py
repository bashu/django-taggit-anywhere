from django.apps import apps
from django.contrib.flatpages.models import FlatPage
from django.test import TestCase

from taggit.managers import TaggableManager

from taggit_anywhere.apps import AppConfig


class AppConfigTest(TestCase):
    """taggit_anywhere.apps.AppConfig.ready() contributes a TaggableManager
    to every model listed in settings.TAGGIT_FOR_MODELS. It already ran once
    during Django startup for this test settings module (TAGGIT_FOR_MODELS =
    ["flatpages.FlatPage"]), so these tests observe that outcome and exercise
    ready() being invoked again.
    """

    def test_tags_manager_added_to_configured_model(self):
        # FlatPage.tags (class-level attribute access) goes through
        # TaggableManager.__get__, which always returns a _TaggableManager
        # instance -- the field itself lives on _meta.
        field = FlatPage._meta.get_field("tags")  # noqa: SLF001

        assert isinstance(field, TaggableManager)

    def test_tagged_model_can_be_used(self):
        page = FlatPage.objects.create(url="/about/", title="About")
        page.tags.add("foo", "bar")

        assert sorted(page.tags.names()) == ["bar", "foo"]

    def test_ready_is_idempotent_when_run_flag_is_set(self):
        # has_run_ready is already True from startup; calling ready() again
        # must be a no-op rather than trying to contribute the field twice.
        app_config = apps.get_app_config("taggit_anywhere")

        assert getattr(AppConfig, "has_run_ready", False)
        app_config.ready()  # would raise if it tried to re-add the field

    def test_ready_skips_models_that_already_have_a_taggable_manager(self):
        # Simulate a fresh run (has_run_ready reset) to exercise the
        # "already tagged" branch instead of the early-return guard.
        field_before = FlatPage._meta.get_field("tags")  # noqa: SLF001

        original = AppConfig.has_run_ready
        AppConfig.has_run_ready = False
        try:
            apps.get_app_config("taggit_anywhere").ready()
        finally:
            AppConfig.has_run_ready = original

        # would be a different object (or raise) had it been re-contributed
        assert FlatPage._meta.get_field("tags") is field_before  # noqa: SLF001
