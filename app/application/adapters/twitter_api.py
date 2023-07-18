import tweepy
from app.config import Settings

settings = Settings()


class TwitterAPI:
    def __init__(self):

        self.consumer_key = settings.TWITTER_CONSUMER_KEY
        self.consumer_secret = settings.TWITTER_CONSUMER_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        self.auth = self._create_auth_handler()
        self.api = tweepy.API(self.auth)

    def _create_auth_handler(self) -> tweepy.OAuthHandler:
        auth = tweepy.OAuthHandler(
            self.consumer_key,
            self.consumer_secret,
        )
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth

    def create_tweet(self, tweet_text: str) -> None:
        try:
            self.api.update_status(tweet_text)
            print("Tweet created successfully!")
        except tweepy.TweepyException as e:
            print("Error creating tweet:", e)

    def list_tweets(self) -> None:
        try:
            tweets = self.api.home_timeline()
            for tweet in tweets:
                print(tweet.text)
        except tweepy.TweepyException as e:
            print("Error listing tweets:", e)

    def delete_tweet(self, tweet_id: str) -> None:
        try:
            self.api.destroy_status(tweet_id)
            print("Tweet deleted successfully!")
        except tweepy.TweepyException as e:
            print("Error deleting tweet:", e)


twitter_api = TwitterAPI()
twitter_api.list_tweets()
# Example usage
# tweet_text = "Hello, Twitter API!"
# twitter_api.create_tweet(tweet_text)
# tweet_id = "1234567890"
# twitter_api.delete_tweet(tweet_id)
