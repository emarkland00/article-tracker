class RedditChildArticleData:
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
        
    def is_self_article(self):
        return self.selftext == None

        
class RedditChildArticle:
    def __init__(self, json):
        self.raw = json
        self.kind = json['kind']
        self.data = RedditChildArticleData(json['data'])

        
class RedditArticleListing:
    def __init__(self, json):
        self.raw = json
        self.modhash = json['modhash']
        self.children = [RedditChildArticle(j) for j in json['children']]
        
    def filter_by_subreddit(self, *subreddits):
        return RedditFilter.by_subreddit(self.children, subreddits)
    
    def filter_by_author(self, *authors):
        return RedditFilter.by_author(authors)
        
class RedditFilter:
    @staticmethod
    def by_subreddit(children, *subreddits):
        subs = subreddits[0]
        for c in children:
            if c.data.subreddit in subs:
                yield c 
        
    @staticmethod
    def by_author(children, *authors):
        a = authors[0]
        for c in children:
            if c.data.author in a:
                yield c