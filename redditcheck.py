import json

import praw

import config

from datetime import datetime, timezone, timedelta

def strip_unicode(s):
    return s.encode('ascii', 'ignore').decode()

class Reddit(object):
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CREDS['client_id'],
            client_secret=config.REDDIT_CREDS['client_secret'],
            password=config.REDDIT_CREDS['password'],
            user_agent=config.REDDIT_CREDS['user_agent'],
            username=config.REDDIT_CREDS['username'],
        )
        self.filter_func = lambda x: x
        print("Successfully logged into reddit as user %s" % self.reddit.user.me())

    def check_subreddit(self, subreddit_name, max_time = None):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = subreddit.new(limit=200)
        except:
            print("Failed to fetch posts.")
            return []
        filtered_posts = self._parse_posts(posts)
        return filtered_posts
    
    def set_filter_func(self, func):
        self.filter_func = func

    def _parse_posts(self, posts):
        formatted_posts = list(map(self._format_post, posts))
        return list(filter(self.filter_func, formatted_posts))

    def _format_post(self, post):
        return {
            'id': strip_unicode(str(post)),
            'title': strip_unicode(post.title),
            'reddit_url': 'reddit.com%s' % strip_unicode(post.permalink),
            'link': strip_unicode(post.url),
            'body': strip_unicode(post.selftext),
            'created': post.created_utc
        }
    