from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import BaseModel


class TaggedItemManager(models.Manager):
    @staticmethod
    def get_tags_for(obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects.select_related('tag') .filter(content_type=content_type, object_id=obj_id)
    @staticmethod
    def get_unavailable_tags(obj_type):
        content_type = ContentType.objects.get_for_model(obj_type)
        return (TaggedItem.objects .select_related('tag')
                .filter(content_type=content_type, tag__available=False))




class Tag(BaseModel):
    label = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.label


class TaggedItem(BaseModel):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
