from django import template
from django.core.cache import cache
from django.conf import settings

register = template.Library()

# from http://djangosnippets.org/snippets/223/
class CachedNode(template.Node):
    """
    Cached template node.

    Subclasses should define the methods ``get_cache_key()`` and
    ``get_content()`` instead of the standard render() method. Subclasses may
    also define the class attribute ``cache_timeout`` to override the default
    cache timeout of ten minutes.
    """

    cache_timeout = 600

    def render(self, context):
        if settings.DEBUG:
            return self.get_content(context)
        key = self.get_cache_key(context)
        content = cache.get(key)
        if not content:
            content = self.get_content(context)
            cache.set(key, content, self.cache_timeout)
        return content

    def get_cache_key(self, context):
        raise NotImplementedError()

    def get_content(self, context):
        raise NotImplementedError()

class ContextUpdatingNode(template.Node):
    """
    Node that updates the context with certain values.

    Subclasses should define ``get_content()``, which should return a dictionary
    to be added to the context.
    """

    def render(self, context):
        context.update(self.get_content(context))
        return ''

class CachedContextUpdatingNode(CachedNode, ContextUpdatingNode):
    """
    Node that updates the context, and is cached. Subclasses need to define
    ``get_cache_key()`` and ``get_content()``.
    """

    def render(self, context):
        context.update(CachedNode.render(self, context))
        return ''