from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_auth.serializers import (
    PasswordResetSerializer as PasswordResetSerializerBase,
)
from rest_framework import exceptions
from rest_framework import serializers

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)
        read_only_fields = ('id', 'email',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_type', 'email', 'first_name', 'last_name',)
        read_only_fields = ('id', 'email',)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(_('A user is already registered with this e-mail address.'))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=True, help_text=_('Email.'))
    password = serializers.CharField(style={'input_type': 'password'}, help_text=_('Password.'))

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_active:
                raise exceptions.ValidationError(_('User account is disabled.'))
        else:
            raise exceptions.ValidationError(_('Unable to log in with provided credentials.'))

        if settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            email_address = user.emailaddress_set.get(email=user.email)
            if not email_address.verified:
                raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(PasswordResetSerializerBase):

    def validate_email(self, email):
        email = super().validate_email(email)
        if email and not email_address_exists(email):
            raise serializers.ValidationError(_('A user with this e-mail address is not registered.'))
        return email

    def get_email_options(self):
        tpl = 'account/email/%s'
        return {
            'subject_template_name': tpl % 'password_reset_subject.txt',
            'email_template_name': tpl % 'password_reset_message.txt',
            'html_email_template_name': tpl % 'password_reset_message.html',
            'extra_email_context': {
                'request': self.context.get('request'),
            }
        }


class VerifyEmailResendSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text=_('Email.'))

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and not email_address_exists(email):
            raise serializers.ValidationError(_('A user with this e-mail address is not registered.'))
        return email

    def save(self, request):
        email_address = EmailAddress.objects.get(email__iexact=self.validated_data.get('email'))
        email_address.send_confirmation(request)
