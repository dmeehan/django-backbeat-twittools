import twitter

from django import template
from django.conf import settings

register = template.Library()

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

class FriendsTimelineNode(node):
    def __init__(self, context_object):
        self.context_object = context_object
    def render(self, context):
        try:
            api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                              consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
            timeline = api.GetFriendsTimeline()
            context[self.context_object] = {
                "name": "%s" % timeline.user.name,
                "screen_name": "%s" % timeline.user.screen_name,
                "avatar": "%s" % timeline.user.profile_image_url,
                "text": "%s" % timeline.text,
                "time": "%s" % timeline.relative_created_at,
                "avatar": "%s" % timeline.user.profile_image_url,
            }

        except:
            context[self.context_object] = {
                "name": "Error",
                "screen_name": "",
                "avatar": "",
                "status": "",
                "time": "",
                "avatar": "",
            }

        return ''