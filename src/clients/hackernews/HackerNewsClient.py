import urlparse
import datetime
import requests
from lxml import etree
from io import StringIO
from clients.TrackerClient import TrackerClient

class HackerNewsClient(TrackerClient):
    KEYS = [ 'BASE_URL', 'USERNAME', 'PASSWORD', 'USER_AGENT' ]
    TRACKER_NAME = 'hacker_news'

    def __init__(self, json_config):
        super(HackerNewsClient, self).__init__(json_config)
        if not json_config:
            return

        self.username = json_config['username']
        self.password = json_config['password']
        self.base_url = json_config['base_url']
        self.user_agent = json_config['user_agent']
        self.session = None

    def __login(self):
        if self.session:
            return

        s = requests.session()
        login = s.get(self.base_url, headers={'User-Agent': self.user_agent })

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

        res = s.post(self.base_url + '/login', headers=headers, data=data)
        self.session = s

    def _get_articles(self):
        posts = self.fetch_upvoted_posts()
        articles = [ self.create_article(p['title'], p['link'], 'hacker news', p['id'], p['timestamp']) for p in posts ]
        return articles

    def fetch_upvoted_posts(self, days_limit=None):
        self.__login()
        arts = []
        url = '{0}/upvoted?id={1}'.format(self.base_url, self.username)
        response = self.session.get(url)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        rows = tree.xpath(".//tr[@class='athing']")
        for row in rows:
            id = row.attrib['id']
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
                day_parts = days_ago.split()
                timestamp = datetime.date.today()
                if day_parts[1] in ['day', 'days']:
                    days_ago = int(day_parts[0])
                    if days_limit and days_ago > days_limit:
                        continue
                    timestamp -= datetime.timedelta(days=int(day_parts[0]))

            arts.append({
                "link": link,
                "title": title,
                "author": author,
                "id": id,
                "timestamp": timestamp
            })

        return arts
