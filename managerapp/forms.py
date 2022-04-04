from django.forms import ModelForm
from .models import ManagerModel, OrderModel
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ManagerForm(ModelForm):
    class Meta:
        model = ManagerModel
        fields = ('first_name',)


class OrderForm(ModelForm):

    class Meta:
        model = OrderModel
        fields = '__all__'
        # widgets = {
        #     "status_order": forms.Select(),
        #     "status_order1": forms.Select(),
        # }

