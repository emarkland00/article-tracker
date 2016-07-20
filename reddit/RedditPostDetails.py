from datetime import datetime

class RedditPostDetails:
    def __init__(self, json):
        self.id = json['id']
        self.subreddit = json['subreddit']
        self.title = json['title']
        self.domain = json['domain']
        self.author = json['author']
        self.created_utc = json['created_utc']
        self.selftext_html = json['selftext_html']
        self.selftext = json['selftext']
        self.url = json['url']
        self.timestamp = datetime.now()

    def is_self_article(self):
        return self.selftext == None
