from RedditPostDetails import RedditPostDetails

class RedditPost:
    def __init__(self, json):
        self.raw = json
        self.kind = json['kind']
        self.data = RedditPostDetails(json['data'])

    def as_json(self):
        return {
            'article_key': self.data.id,
            'name': self.data.title,
            'url': self.data.url,
            'timestamp': self.data.timestamp
        }
