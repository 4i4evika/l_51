from django.forms import ModelForm
from .models import Shop


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'image', 'description', 'memo']