import sched
import time
from datetime import datetime, timedelta

from redditcheck import Reddit
from notifier import Notifier
import config

class BuildAPcWatch(object):
    def __init__(self, max_age_hours = None):
        self.reddit = Reddit()
        self.reddit.set_filter_func(self._filter_post)
        self.seen_posts = []
        self.notifier = Notifier()
        self.first_run = True
        self.max_age_hours = max_age_hours

    def watch(self):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(config.UPDATE_FREQUENCY, 1, self._update, (s, ))
        s.run()

    def _update(self, s):
        print("%s : Updating..." % str(datetime.now()))
        interested_posts = self.reddit.check_subreddit('buildapcsales')
        new_posts = self._identify_new_posts(interested_posts)
        if new_posts:
            self._update_history(new_posts)
            if not self.first_run:
                print("Found interesting posts, sending notifications...")
                self._handle_new_posts(new_posts)
            else:
                self.first_run = False
                print("Ignoring the following posts on first cycle:")
                for post in new_posts:
                    print(post['title'])
        s.enter(config.UPDATE_FREQUENCY, 1, self._update, (s, ))

    def _identify_new_posts(self, posts):
        filter_seen = lambda post: not (post['id'] in self.seen_posts)
        return list(filter(filter_seen, posts))

    def _handle_new_posts(self, new_posts):
        for post in new_posts:
            self.notifier.alert(post)

    def _update_history(self, new_posts):
        self.seen_posts.extend(list(map(lambda p: p['id'], new_posts)))

    def _filter_post(self, post):
        if self.max_age_hours:
            max_age = datetime.utcnow() - timedelta(hours = self.max_age_hours)
            if datetime.fromtimestamp(post['created']) > max_age:
                return
        if not any(keyword in post['title'] for keyword in config.KEYWORDS):
            return
        return post

if __name__ == '__main__':
    BuildAPcWatch(max_age_hours=1).watch()