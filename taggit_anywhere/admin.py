# -*- coding: utf-8 -*-

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


for model_name in getattr(settings, 'TAGGIT_FOR_MODELS', []):
    from django.contrib.admin.sites import site as default_site

    model = apps.get_model(*model_name.rsplit('.', 1))

    try:
        modeladmin = default_site._registry[model].__class__
    except KeyError:
        raise ImproperlyConfigured(
            "Please put ``taggit_anywhere`` in your settings.py only as last INSTALLED_APPS")

    default_site.unregister(model)
    
    FIELDSET_TAGS = (None, {
        'fields': (
            'tags',
        ),
    })

    class TaggedAdmin(modeladmin):
        fieldsets = getattr(modeladmin, 'fieldsets', [])

    if TaggedAdmin.fieldsets is not None:
        TaggedAdmin.fieldsets = list(TaggedAdmin.fieldsets)[:] + [FIELDSET_TAGS]

    if 'taggit_helpers' in settings.INSTALLED_APPS:
        from taggit_helpers.admin import TaggitListFilter
        
        TaggedAdmin.list_filter = list(TaggedAdmin.list_filter)[:] + [TaggitListFilter]
                    
    if 'taggit_labels' in settings.INSTALLED_APPS:
        from taggit_labels.widgets import LabelWidget
        from taggit.forms import TagField

        class TaggedAdminForm(TaggedAdmin.form):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for f in self.fields:
                    if not issubclass(self.fields[f].__class__, TagField):
                        continue
                    if not issubclass(self.fields[f].widget.__class__, LabelWidget):
                        self.fields[f].widget = LabelWidget()

        TaggedAdmin.form = TaggedAdminForm

    default_site.register(model, TaggedAdmin)
