from django import apps
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured

from .importpath import importpath
    

class AppConfig(apps.AppConfig):
    name = 'taggit_anywhere'

    def ready(self):
        # Ensure everything below is only ever run once
        if getattr(AppConfig, 'has_run_ready', False):
            return
        AppConfig.has_run_ready = True

        from django.conf import settings
        from taggit.managers import TaggableManager
    
        FIELDSET_TAGS = (None, {
            'fields': ('tags',),
        })

        for model_name in getattr(settings, 'TAGS_FOR_MODELS', []):
            model = importpath(model_name, 'TAGS_FOR_MODELS')

            model.add_to_class('tags', TaggableManager(blank=True))

            try:
                model_admin = admin.site._registry[model].__class__
            except KeyError:
                raise ImproperlyConfigured(
                    "Please put ``taggit_anywhere`` in your settings.py only as last INSTALLED_APPS")
            admin.site.unregister(model)

            setattr(model_admin, 'fieldsets', getattr(model_admin, 'fieldsets', []))
            if model_admin.fieldsets is not None:
                model_admin.fieldsets = list(model_admin.fieldsets)[:] + [FIELDSET_TAGS]

            admin.site.register(model, model_admin)

