from RedditPostDetails import RedditPostDetails

class RedditPost:
    def __init__(self, json):
        self.raw = json
        self.kind = json['kind']
        self.data = RedditPostDetails(json['data'])

    def to_article(self):
        return {
            'article_key': self.data.id,
            'name': self.data.title,
            'url': self.data.url,
            'source': 'reddit',
            'timestamp': self.data.timestamp
        }
