import importlib
import re
from collections.abc import Iterator
from http import HTTPStatus

from django.contrib.admin.sites import site as default_site
from django.contrib.auth.models import User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ImproperlyConfigured
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse

import pytest
from pytest_django.asserts import assertContains
from taggit.forms import TagField
from taggit_helpers.admin import TaggitListFilter
from taggit_labels.widgets import LabelWidget

from taggit_anywhere import admin as taggit_anywhere_admin


@pytest.fixture
def url_flatpage_add() -> str:
    return reverse("admin:flatpages_flatpage_add")


@pytest.mark.django_db
class TestAdminRegistration:
    """taggit_anywhere.admin patches the already-registered ModelAdmin for
    every model in settings.TAGGIT_FOR_MODELS (FlatPage here), adding a
    "tags" fieldset, a tag list filter and (when taggit_labels is installed)
    a label widget for the tags field. The fieldset/list_filter patch is
    baked into the ModelAdmin class at import time; the form fields are only
    rebuilt from the model's *current* fields when ModelAdmin.get_form() runs
    (that's what actually picks up the "tags" field, which taggit_anywhere's
    own AppConfig.ready() adds later than admin autodiscovery), so form
    assertions go through get_form() rather than instantiating .form directly.
    """

    @pytest.fixture(autouse=True)
    def setup(
        self,
        rf: RequestFactory,
        admin_user: User,
        url_flatpage_add: str,
    ) -> None:
        self.model_admin = default_site._registry[FlatPage]  # noqa: SLF001
        request = rf.get(url_flatpage_add)
        request.user = admin_user
        self.form_class = self.model_admin.get_form(request)

    def test_replaces_registration_with_a_subclass(self) -> None:
        assert type(self.model_admin).__name__ == "TaggedAdmin"
        assert type(self.model_admin).__name__ != "FlatPageAdmin"

    def test_adds_tags_fieldset(self) -> None:
        fieldsets = self.model_admin.fieldsets

        assert fieldsets[-1] == (None, {"fields": ("tags",)})
        # the original FlatPageAdmin fieldsets are preserved ahead of it
        assert len(fieldsets) > 1

    def test_adds_taggit_list_filter(self) -> None:
        assert TaggitListFilter in self.model_admin.list_filter
        # original list_filter entries are preserved
        assert "registration_required" in self.model_admin.list_filter

    def test_tags_field_uses_label_widget(self) -> None:
        form = self.form_class()

        tag_fields = [
            field for field in form.fields.values() if isinstance(field, TagField)
        ]
        assert len(tag_fields) == 1
        assert isinstance(tag_fields[0].widget, LabelWidget)

    def test_other_form_fields_keep_their_default_widget(self) -> None:
        form = self.form_class()

        assert not isinstance(form.fields["url"].widget, LabelWidget)


@pytest.mark.django_db
class TestAdminIntegration:
    """End-to-end smoke test that the patched admin actually renders and
    saves tags through the normal admin add view."""

    def test_add_view_renders_tags_widget(
        self,
        admin_client: Client,
        url_flatpage_add: str,
    ) -> None:
        response = admin_client.get(url_flatpage_add)

        assert response.status_code == HTTPStatus.OK
        assertContains(response, "taggit-labels")

    def test_add_view_saves_tags(
        self,
        admin_client: Client,
        url_flatpage_add: str,
    ) -> None:
        response = admin_client.post(
            url_flatpage_add,
            {
                "url": "/about/",
                "title": "About",
                "content": "",
                "sites": [1],
                "tags": "foo, bar",
                "template_name": "",
            },
        )

        assert response.status_code == HTTPStatus.FOUND
        page = FlatPage.objects.get(url="/about/")
        assert sorted(page.tags.names()) == ["bar", "foo"]


class TestAdminImportGuard:
    """taggit_anywhere/admin.py runs its registration loop at import time,
    so it can only patch a ModelAdmin that some other app already
    registered -- that's why the docs say to list ``taggit_anywhere`` last.
    Reload the module with the target unregistered to exercise that guard.
    """

    @pytest.fixture(autouse=True)
    def restore_registration(self) -> Iterator[None]:
        yield

        # Whatever the reload attempt left behind, put back a single,
        # freshly-wrapped registration so later tests see the same state
        # they would have without this test running at all.
        if FlatPage in default_site._registry:  # noqa: SLF001
            default_site.unregister(FlatPage)

        default_site.register(FlatPage, FlatPageAdmin)
        importlib.reload(taggit_anywhere_admin)

    def test_raises_when_target_model_is_not_already_registered(self) -> None:
        default_site.unregister(FlatPage)

        message = (
            "Please put ``taggit_anywhere`` in your settings.py only as last "
            "INSTALLED_APPS"
        )

        with pytest.raises(ImproperlyConfigured, match=re.escape(message)):
            importlib.reload(taggit_anywhere_admin)
