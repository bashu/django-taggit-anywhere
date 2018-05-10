# -*- coding: utf-8 -*-

from django.apps import apps
from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    name = 'taggit_anywhere'

    def ready(self):
        # Ensure everything below is only ever run once
        if getattr(AppConfig, 'has_run_ready', False):
            return
        AppConfig.has_run_ready = True

        from django.conf import settings

        from taggit.managers import TaggableManager
    
        for model_name in getattr(settings, 'TAGGIT_FOR_MODELS', []):
            model = apps.get_model(*model_name.rsplit('.', 1))

            if hasattr(model, 'tags'):
                if isinstance(getattr(model, 'tags'), TaggableManager):
                    # the attribute is already an instance of the class
                    # we want.
                    continue

            TaggableManager(blank=True).contribute_to_class(model, 'tags')
