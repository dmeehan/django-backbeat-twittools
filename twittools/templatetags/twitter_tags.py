import twitter
import re

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib import messages
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

register = Library()

@register.filter
def parse_tweet(value):
    """
        http://djangosnippets.org/snippets/2161/
        A simple template filter for parsing tweets
        (linking @ replies, hashtages and standard URLs)
    """
    value = re.sub(r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)', '<a href="\g<0>" rel="external">\g<0></a>', value)
    value = re.sub(r'http://(yfrog|twitpic).com/(?P<id>\w+/?)', '', value)
    value = re.sub(r'#(?P<tag>\w+)', '<a href="http://search.twitter.com/search?tag=\g<tag>" rel="external">#\g<tag></a>', value)
    value = re.sub(r'@(?P<username>\w+)', '@<a href="http://twitter.com/\g<username>/" rel="external">\g<username></a>', value)

    return mark_safe(value)

@register.tag(name="get_friends_timeline")
def do_get_friends_timeline(parser, token):
    """
    Call this tag with:
        get_friends_timeline as <context_object>

    TODO: Add caching
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0]
    if bits[1] != "as":
        raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0]
    return FriendsTimelineNode(bits[2])

class FriendsTimelineNode(Node):
    def __init__(self, context_object):
        self.context_object = context_object
    def render(self, context):

        try:
            api = twitter.Api(consumer_key='%s' % settings.TWITTER_CONSUMER_KEY, consumer_secret='%s' % settings.TWITTER_CONSUMER_SECRET, access_token_key= '%s' % settings.TWITTER_ACCESS_TOKEN_KEY, access_token_secret='%s' % settings.TWITTER_ACCESS_TOKEN_SECRET)

            context[self.context_object] = api.GetFriendsTimeline()

        except:
            context[self.context_object] = {
                }

        return ''