from django.urls import path, include
{%- if cookiecutter.use_allauth == "y" and cookiecutter.use_rest == "y" %}
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
{%- endif %}
from users import views

urlpatterns = [
{%- if cookiecutter.use_allauth == "y" and cookiecutter.use_rest == "y" %}
    path('auth/', include((
        [
            path('registration/', views.registration, name='registration'),
            path('login/', obtain_jwt_token, name='login'),
            path('logout/', views.logout, name='logout'),
            path('token_refresh/', refresh_jwt_token, name='token_refresh'),
            path('token_verify/', verify_jwt_token, name='token_verify'),
            path('password_change/', views.password_change, name='password_change'),
        ], 'users'), namespace='auth')),
{%- endif %}
    path('users/', include((
        [

        ], 'users'), namespace='users')),
]
