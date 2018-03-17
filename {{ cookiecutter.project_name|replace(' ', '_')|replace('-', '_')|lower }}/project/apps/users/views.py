{%- if cookiecutter.use_allauth == "y" and cookiecutter.use_rest == "y" %}
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_auth.app_settings import create_token
from rest_auth.registration.views import RegisterView as RegisterViewBase
from rest_auth.views import PasswordChangeView as BasePasswordChangeView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.jwt import jwt_response_payload_handler


class RegisterApiView(RegisterViewBase):
    """
    Generic user registration.

    """

    http_method_names = ('post', 'head', 'options')
    permission_classes = (AllowAny,)

    def get_response_data(self, user):
        token = create_token(user)
        data = jwt_response_payload_handler(token, user)
        return data


class LogoutApiView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.

    """

    http_method_names = ('post', 'head', 'options')
    permission_classes = (AllowAny,)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        auth_logout(request)

        return Response({'detail': _('Successfully logged out.')}, status=status.HTTP_200_OK)


class PasswordChangeApiView(BasePasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: old_password, new_password1, new_password2
    Returns the success/fail message.

    """

    http_method_names = ('post', 'head', 'options')
    permission_classes = (IsAuthenticated,)


registration = RegisterApiView.as_view()

logout = LogoutApiView.as_view()

password_change = PasswordChangeApiView.as_view()
{%- endif %}
