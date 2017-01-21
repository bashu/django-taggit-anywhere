from django.db import models

from taggit.models import GenericTaggedItemBase, TagBase


class SkillTag(TagBase):
    pass


class SkillTaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(SkillTag, related_name="skills")
