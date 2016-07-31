from RedditPost import RedditPost
from mysql import Article

class RedditPostListing:
    def __init__(self, json):
        self.raw = json
        self.modhash = json['modhash']
        self.raw_children = [RedditPost(j) for j in json['children']]
        self.children = self.raw_children
