import autocomplete_light
from .models import Category

class CategoryAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name']
    model = Category