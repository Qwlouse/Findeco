from django.contrib.syndication.views import Feed
from microblogging.views import *
from django.utils.feedgenerator import Atom1Feed
from django.contrib.auth.models import *
from models import UserProfile
from microblogging.models import Post
from django.shortcuts import get_object_or_404
def rsskeyIsValid( rsskey , name):
    user= User.objects.get(username=name)
    if rsskey==user.profile.verification_key[:8]:
        return  True
    else:
        return False

class RssFeed(Feed):
    feed_url = "http://www.mydomain.com/blog/rss"
    title = "Findeco Test-Feed"
    link = "/rss/"
    description = "Inhalte des Findeco Systems"
    def item_title(self, item):
        
        return item.author.username + " schreibt:"
    #def item_author_name(self, item):
        #return item.author.username
    #def item_author_link(self, item):
    #    return "http://localhost:8000/#/user/" + item.author.username
    def item_link(self, item):
        return ""
    def item_date(self, item):
        return item.time
    def item_description(self,item):
        return item.text
    def item_pubdate(self, item):
        return item.time
    def get_object(self, request, rsstype , rsskey , name):
        if rsskeyIsValid(rsskey , name):
            if rsstype =="timeline":
                return get_timeline(name, 50)
            if rsstype =="mention":
                return get_mentions(name, 50)  #Checked!!!!
            if rsstype =="news":
                return get_news()
            if rsstype =="newsAuthor":
                return get_newsAuthor(name, 50)
            if rsstype =="newsFollow":
                return get_newsFollow(name, 50)
        
        else:
            err = Post()
            err.title = "Non Matching Path"
            err.author.username="System"
            return [err]
            '''@todo: This should be outputted as RSS Feed currently it displays as 404'''
        
    def items(self ,obj):
        #
        #    return get_mentions("admin", 50)
        #else:
         #   '''Here we need to do something'''
        return obj
    
class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description