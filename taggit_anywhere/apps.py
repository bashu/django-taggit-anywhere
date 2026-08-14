from django.apps import AppConfig as DefaultAppConfig
from django.apps import apps


class AppConfig(DefaultAppConfig):
    name = "taggit_anywhere"

    def ready(self):
        # Ensure everything below is only ever run once
        if getattr(AppConfig, "has_run_ready", False):
            return
        AppConfig.has_run_ready = True

        # deferred: AppConfig modules are imported before the app registry
        # is ready, so app/model imports have to wait until ready() runs.
        from django.conf import settings  # noqa: PLC0415
        from django.core.exceptions import FieldDoesNotExist  # noqa: PLC0415

        from taggit.managers import TaggableManager  # noqa: PLC0415

        for model_name in getattr(settings, "TAGGIT_FOR_MODELS", []):
            model = apps.get_model(*model_name.rsplit(".", 1))

            try:
                field = model._meta.get_field("tags")  # noqa: SLF001
            except FieldDoesNotExist:
                field = None

            if isinstance(field, TaggableManager):
                # the field is already an instance of the class we want.
                continue

            TaggableManager(blank=True).contribute_to_class(model, "tags")
