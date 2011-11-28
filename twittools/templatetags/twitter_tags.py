import twitter

from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings

register = Library()

@register.tag(name="get_friends_timeline")
def do_get_friends_timeline(parser, token):
    """
    Call this tag with:
        get_friends_timeline as <context_object>
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
            api = twitter.Api(consumer_key='%s' % settings.TWITTER_CONSUMER_KEY,
                              consumer_secret='%s' % settings.TWITTER_CONSUMER_SECRET,
                              access_token_key= '%s' % settings.TWITTER_ACCESS_TOKEN_KEY,
                              access_token_secret='%s' % settings.TWITTER_ACCESS_TOKEN_SECRET)
            timeline = api.GetFriendsTimeline()
            context[self.context_object] = timeline

        except:
            context[self.context_object] = {
                
            }

        return ''