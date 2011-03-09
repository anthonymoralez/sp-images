from xml.sax.saxutils import escape
import feedparser

def upgrade_feed():
    original_feed = feedparser.parse("http://www.somethingpositive.net/sp.xml")
    upgraded_links = []

    for item in original_feed.entries:
        upgraded_links.append( (item, item.link.replace("shtml", "png")))

    rss = u"""<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Something Positive by R.K. Milholland</title>
    <link>http://www.somethingpositive.net</link>
    <description>Comics strips, news updates, and convention schedule for the webcomic Something Positive.</description>
    <copyright>(c) 2001-2009 R.K. Milholland</copyright>
    <managingEditor>choochoobear@gmail.com</managingEditor>
    <lastBuildDate>%s</lastBuildDate>""" % original_feed.channel.updated
    for entry, image_link in upgraded_links:
        rss += u"""
    <item>
      <title>%s</title>
      <link>%s</link>
      <description>
        <![CDATA[<a href="%s"><img src="%s" /></a>]]>
      </description>
    </item>
""" % (escape(entry.title), escape(entry.link), escape(entry.link), escape(image_link))

    rss += u"""
  </channel>
</rss>"""
    return rss

print upgrade_feed()
