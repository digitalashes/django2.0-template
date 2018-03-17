import coreapi
from rest_framework.compat import (
    URLPattern,
    URLResolver,
)
from rest_framework.compat import get_original_route
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.generators import (
    EndpointEnumerator,
    distribute_links,
)


class CustomCoreApiDocument(coreapi.Document):
    def __init__(self, *args, **kwargs):
        links = kwargs.pop('links', None)
        super().__init__(*args, **kwargs)
        self._links = links

    @property
    def unsorted_links(self):
        data = {}
        links = []
        for section_key, section_values in sorted(self._links.items()):
            data.update({section_key: []})
            for link_key, link_values in section_values.items():
                if hasattr(link_values, 'links'):
                    links.extend([
                        {'link_key': f'{link_key} > {i[0]}', 'url': i[1].url, 'action': f'{link_key}/{i[0]}'}
                        for i in link_values.links
                    ])
                else:
                    links.append({'link_key': f'{link_key}', 'url': link_values.url, 'action': link_key})
            data.update({section_key: links.copy()})
            links.clear()
        return data


class CustomEndpointEnumerator(EndpointEnumerator):
    """
        Fixed sorting urls by alphabet.

    """

    def get_api_endpoints(self, patterns=None, prefix=''):
        """
        Return a list of all available API endpoints by inspecting the URL conf.
        """
        if patterns is None:
            patterns = self.patterns

        api_endpoints = []

        for pattern in patterns:
            path_regex = prefix + get_original_route(pattern)
            if isinstance(pattern, URLPattern):
                path = self.get_path_from_regex(path_regex)
                callback = pattern.callback
                if self.should_include_endpoint(path, callback):
                    for method in self.get_allowed_methods(callback):
                        endpoint = (path, method, callback)
                        api_endpoints.append(endpoint)

            elif isinstance(pattern, URLResolver):
                nested_endpoints = self.get_api_endpoints(
                    patterns=pattern.url_patterns,
                    prefix=path_regex
                )
                api_endpoints.extend(nested_endpoints)

        return api_endpoints


class CustomGenerator(SchemaGenerator):
    """
    Fixes DRF fail if custom `schema` definition in @detail_route provided.
    """

    endpoint_inspector_cls = CustomEndpointEnumerator

    def create_view(self, callback, method, request=None):
        view = super().create_view(callback, method, request)
        view.schema.view = view
        return view

    def get_schema(self, request=None, public=False):
        """
        Generate a `coreapi.Document` representing the API schema.
        """
        if self.endpoints is None:
            inspector = self.endpoint_inspector_cls(self.patterns, self.urlconf)
            self.endpoints = inspector.get_api_endpoints()

        links = self.get_links(None if public else request)
        if not links:
            return None

        url = self.url
        if not url and request is not None:
            url = request.build_absolute_uri()

        distribute_links(links)
        return CustomCoreApiDocument(
            title=self.title, description=self.description,
            url=url, content=links, links=links,
        )


docs = include_docs_urls(
    generator_class=CustomGenerator,
    title='{{ cookiecutter.project_name|capitalize }} API',
    description='{{ cookiecutter.project_name|capitalize }} endpoints',
    authentication_classes=[],
    permission_classes=[],
)
