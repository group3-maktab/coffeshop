from django.contrib.contenttypes.models import ContentType
from django.db.models import F

from foodmenu.models import Category, Food
from tag.models import TaggedItemManager, TaggedItem


class FoodTagModel(Food):
    @staticmethod
    def update_availability_based_on_tags():
        Food.objects.update(availability=True)
        unavailable_tags = TaggedItem.objects.get_unavailable_tags(Food)
        content_type = ContentType.objects.get_for_model(Food)
        object_ids = [tag.object_id for tag in unavailable_tags if tag.content_type == content_type]

        # Now you have a list of object_ids that have unavailable tags
        food_objects = Food.objects.filter(id__in=object_ids)
        food_objects.update(availability=False)


