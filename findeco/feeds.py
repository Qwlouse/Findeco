from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from microblogging.models import Post
class RssFeed(Feed):
    title = "Findeco Test-Feed"
    link = "/rss/"
    description = "Inhalte des Findeco Systems"

    
    def item_title(self, item):
        return item.text
    def item_author_name(self, item):
        return item.author

    def item_link(self, item):
        
        return item.text
    def item_date(self, item):
        return item.date
    def items(self):
        feed = Post.objects.order_by('-time')
        return feed
    
class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description