from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

{%- if cookiecutter.use_rest == "y" %}
from config.api_docs import docs

api_urlpatterns = [
    path('', include('users.urls')),
]
{%- endif %}

urlpatterns = [
{%- if cookiecutter.use_rest == "y" %}
    path('', RedirectView.as_view(url='/api/docs/'), name='index'),
{%- endif %}
    path(settings.ADMIN_URL, admin.site.urls),
{% if cookiecutter.use_rest == "y" %}
    path('api/docs/', docs),
    path('api/', include(arg=(api_urlpatterns, 'config'), namespace='api')),
{%- endif %}
]

if settings.USE_SILK:
    urlpatterns += [
        path('silk/', 'silk.urls')
    ]

if settings.USE_DEBUG_TOOLBAR:
    urlpatterns += [
        path('__debug__/', 'debug_toolbar.urls'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
