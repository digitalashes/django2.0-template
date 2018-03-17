from allauth.account.models import EmailAddress
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class EmailAddressStackedInline(admin.StackedInline):
    model = EmailAddress
    fields = ('email', 'verified', 'primary',)
    extra = 0


class UserChangeForm(UserChangeFormBase):
    class Meta(UserChangeFormBase.Meta):
        model = User
        fields = '__all__'


class UserCreationForm(UserCreationFormBase):
    error_message = UserCreationFormBase.error_messages.update({
        'duplicate_email': 'This email has already been taken.'
    })

    class Meta(UserCreationFormBase.Meta):
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    inlines = (EmailAddressStackedInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': (
                'email', 'first_name', 'last_name', 'password', 'last_login', 'date_joined')
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        })
    )
