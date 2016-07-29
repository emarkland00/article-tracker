import requests
from config import ConfigClass
from lxml import etree
from io import StringIO
import urlparse

class HackerNewsClient:
    def __init__(self):
        hn_config = ConfigClass().get_hacker_news_config()
        if not hn_config:
            print "Unable to fetch content from hacker news"
            return

        self.username = hn_config['username']
        self.password = hn_config['password']
        self.base_url = hn_config['base_url']
        self.user_agent = hn_config['user_agent']
        self.session = None

    def __login(self):
        if self.session:
            return

        s = requests.session()
        login = s.get(self.base_url, verify=False, headers={'User-Agent': self.user_agent })

        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': self.base_url
        }

        vals = {
            "goto": "news",
            "acct": self.username,
            "pw": self.password
        }
        data = "&".join([ "{0}={1}".format(key,vals[key]) for key in vals ])

        res = s.post(self.base_url + '/login', verify=False, headers=headers, data=data)
        self.session = s

    def fetch_upvoted_articles(self):
        self.__login()
        arts = []
        url = '{0}/upvoted?id={1}'.format(self.base_url, self.username)
        response = self.session.get(url)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        rows = tree.xpath(".//tr[@class='athing']")
        for row in rows:
            #import pdb; pdb.set_trace()
            header = row.xpath(".//td[@class='title']/a")[0]
            link = header.attrib['href']
            link = (self.base_url + "/" + link) if not bool(urlparse.urlparse(link).netloc) else link
            title = header.text
            author = None
            timestamp = None
            author_row = row.xpath(".//following-sibling::tr//td[@class='subtext']")
            if author_row:
                ar = author_row[0]
                author = ar.xpath(".//a[@class='hnuser']")[0].text
                days_ago = ar.xpath(".//span[@class='age']//a")[0].text

            arts.append({
                "link": link,
                "title": title,
                "author": author,
                "timestamp": timestamp
            })

        return arts

    # maybe get reports for the last 30 DAYS?
