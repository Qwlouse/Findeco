from django.contrib.syndication.views import Feed
from microblogging.views import *
from django.utils.feedgenerator import Atom1Feed
from microblogging.models import Post
import hashlib
from findeco.settings import FINDECO_BASE_URL


def rsskeyIsValid(rsskey, name):
    user = User.objects.get(username=name)
    if rsskey == user.profile.api_key:
        return True
    else:
        return False


class RssFeed(Feed):
    item_guid_is_permalink = False

    def item_title(self, item):
        return item.author.username + ": " + item.text
    #def item_author_name(self, item):
        #return item.author.username
    #def item_author_link(self, item):
    #    return "http://localhost:8000/user/" + item.author.username

    def item_link(self, item):
        # return item
        return "http://www.findeco.de"

    def item_guid(self, item):
        return hashlib.md5(unicode(item.time) +
                           item.author.username).hexdigest()

    def item_guid_is_permalink(self, item):
        return False

    def item_date(self, item):
        return item.time

    def item_description(self, item):
        return item.text

    def item_pubdate(self, item):
        return item.time

    def get_object(self, request, rsstype , rsskey , name):
        self.rsstype = rsstype

        if rsskeyIsValid(rsskey, name):
            self.link = FINDECO_BASE_URL + "/feeds/rss/timeline/" + name + "/rsskey/"
            self.feed_url = self.link
            self.feed_guid = hashlib.md5(self.link)

            if rsstype == "timeline":
                self.title = "Findeco - Timeline"
                self.description = "Deine Findeco Timeline"
                return get_timeline(name, 50)
            if rsstype == "mention":
                self.title = "Findeco - Mentions"
                self.description = "Deine Findeco Mentions"
                return get_mentions(name, 50)  # Checked!!!!
            if rsstype == "news":
                self.title = "Findeco - News"
                self.description = "Deine Findeco News"
                return get_news()
            if rsstype == "newsAuthor":
                self.title = "Findeco - Autor News"
                self.description = "Deine Findeco Autor News"
                return get_newsAuthor(name, 50)
            if rsstype == "newsFollow":
                self.title = "Findeco - Folge News"
                self.description = "Deine Findeco Folge News"
                return get_newsFollow(name, 50)
        
        else:
            err = Post()
            err.title = "Non Matching Path"
            err.author.username = "System"
            return [err]
            #todo: This should be outputted as RSS Feed currently it
            #      displays as 404
        
    def items(self, obj):
        #
        #    return get_mentions("admin", 50)
        #else:
         #   '''Here we need to do something'''
        return obj


class AtomFeed(RssFeed):
    feed_type = Atom1Feed
#    subtitle = RssFeed.description
