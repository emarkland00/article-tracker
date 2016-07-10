from RedditPost import RedditPost

class RedditPostListing:
    def __init__(self, json):
        self.raw = json
        self.modhash = json['modhash']
        self.raw_children = [RedditPost(j) for j in json['children']]
        self.children = self.raw_children

    def filter_by_new_listings(self):
        keys = [ c.data.id for c in self.children ]
        results = Article.select().where(Article.article_key << keys)
        existing_keys = [ r.article_key for r in results ]
        self.children = [c for c in self.children if c.data.id not in existing_keys]
        return self

    def filter_by_subreddit(self, *subreddits):
        return [ c for c in self.children if c.data.subreddit in subreddits ]
