import logging

from django import forms
from django.forms import ModelForm
from django.conf import settings

from tansu.models import Entity, AudioFile, DocumentFile, ImageFile, VideoFile

logger = logging.getLogger(__name__)


class EntityEditForm(ModelForm):
    class Meta:
        model = Entity
