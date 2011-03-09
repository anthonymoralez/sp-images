import os
import upgrade_feed

from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Feed(db.Model):
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class Root(webapp.RequestHandler):
    def get(self):
        feeds = Feed.gql("ORDER BY date DESC LIMIT 1")
        if feeds.count() == 1:
            feed = feeds[0]
            yesterday = datetime.today() - timedelta(1)
            if feed.date < yesterday: 
                feed.content = upgrade_feed.upgrade_feed()
                feed.date = datetime.today() 
                feed.put()
        else:
            feed = Feed()
            feed.content = upgrade_feed.upgrade_feed()
            feed.put()
        self.response.out.write(feed.content)
        

application = webapp.WSGIApplication( [ ('/sp.xml', Root) ], debug=True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
