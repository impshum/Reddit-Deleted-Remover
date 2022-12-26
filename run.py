import praw
import configparser
from pmaw import PushshiftAPI


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
target_subreddits = [x.strip() for x in config['SETTINGS']['target_subreddits'].split(',')]
post_limit = int(config['SETTINGS']['post_limit'])
delete_submissions = config['SETTINGS'].getboolean('delete_submissions')
delete_comments = config['SETTINGS'].getboolean('delete_comments')
test_mode = config['SETTINGS'].getboolean('test_mode')

reddit = praw.Reddit(
    username=reddit_user,
    password=reddit_pass,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='Reddit Deleted Remover (by u/impshum)'
)

api = PushshiftAPI()


def deleter(target_subreddit, type):
    print(f'Searching r/{target_subreddit} {type}s')
    if type == 'submission':
        posts = api.search_submissions(subreddit=target_subreddit, author='[deleted]', filter=['id'], limit=post_limit)
    else:
        posts = api.search_comments(subreddit=target_subreddit, author='[deleted]', filter=['id'], limit=post_limit)

    for post in [post for post in posts]:
        post_id = post['id']
        print(f'Deleting {type} {post_id} from r/{target_subreddit}')
        if not test_mode:
            if type == 'submission':
                reddit_post = reddit.submission(post_id)
            else:
                reddit_post = reddit.comment(post_id)
            reddit_post.delete()


def main():
    if test_mode:
        print('TEST MODE')

    types = []
    if delete_submissions:
        types.append('submission')
    if delete_comments:
        types.append('comment')

    for target_subreddit in target_subreddits:
        for type in types:
            deleter(target_subreddit, type)


if __name__ == '__main__':
    main()
