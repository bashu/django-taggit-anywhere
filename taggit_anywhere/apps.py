# -*- coding: utf-8 -*-

from django.contrib import admin
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps


class AppConfig(AppConfig):
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

        for value in getattr(settings, 'TAGGIT_FOR_MODELS', []):
            Model = apps.get_model(*value.rsplit('.', 1))

            Model.add_to_class('tags', TaggableManager(blank=True))

            try:
                ModelAdmin = admin.site._registry[Model].__class__
            except KeyError:
                raise ImproperlyConfigured(
                    "Please put ``taggit_anywhere`` in your settings.py only as last INSTALLED_APPS")
            admin.site.unregister(Model)

            setattr(ModelAdmin, 'fieldsets', getattr(ModelAdmin, 'fieldsets', []))
            if ModelAdmin.fieldsets is not None:
                ModelAdmin.fieldsets = list(ModelAdmin.fieldsets)[:] + [FIELDSET_TAGS]

            if 'taggit_helpers' in settings.INSTALLED_APPS:
                from taggit_helpers.admin import TaggitListFilter
                
                class ModelAdmin(ModelAdmin):
                    list_filter = list(ModelAdmin.list_filter)[:] + [TaggitListFilter]

            if 'taggit_labels' in settings.INSTALLED_APPS:
                from taggit.forms import TagField
                from taggit_labels.widgets import LabelWidget

                class ModelForm(ModelAdmin.form):
                    tags = TagField(required=False, widget=LabelWidget)
                
                class ModelAdmin(ModelAdmin):
                    form = ModelForm
                    
            admin.site.register(Model, ModelAdmin)
