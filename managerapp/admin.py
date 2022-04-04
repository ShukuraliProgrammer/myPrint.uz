from django.contrib import admin
from .models import ManagerModel, OrderModel
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ManagerModel
        fields = ('email', 'date_of_birthday', 'first_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password1")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=False):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = ManagerModel
        fields = ('email', 'password', 'date_of_birthday', 'is_active', 'is_admin', 'first_name')

    def clean_password(self):
        return self.initial["password"]


class ManagerAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('first_name','email', 'date_of_birthday', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name')}),
        ('Personal info',
         {'fields': ('date_of_birthday',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('widget',),
            'fields': ('email', 'first_name',
                       'date_of_birthday', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(ManagerModel, ManagerAdmin)
admin.site.unregister(Group)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'manager','customer', 'created', 'limit']

    list_display = ['customer', 'phone', 'created', 'limit', 'product', 'number', 'price', 'percent', 'status_order']

    def has_delete_permission(self, request, obj=None):
        return False
