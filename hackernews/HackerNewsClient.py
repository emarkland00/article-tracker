import requests
from config import ConfigClass

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

    def __login(self):
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
        data = "&".join([ "{0}={1}".format(k,v) for k,v in vals ])

        res = s.post(self.base_url + '/login', verify=False, headers=headers, data=data)
        t = res.text

    def fetch_upvoted_articles(self):
        url = '{0}/saved?id={1}'.format(self.base_url, self.username)
        response = self.session.get(url)
        tree = html.fromstring(response.text)
        tables = tree.xpath("//table")
        for t in tables:
            post = t.xpath("//tr[contains('@class', 'athing')]")
            if len(post) is 0:
                continue

            header = post.xpath("//td[@class='title']/a")
            link = header.attr('href')
            title = header.value
            author = post.xpath("//span").value
    # maybe get reports for the last 30 DAYS?
