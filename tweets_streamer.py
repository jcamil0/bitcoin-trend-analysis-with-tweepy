import tweepy
import json

consumer_key = "BwV6HVigRpdNHEqwK6uK3RxCg"
consumer_secret = "XoHFc5kGm8EgVauSN9JXLHDgdwyjtzQqgNYbnJZy7dXnh2iInz"
access_key = "628480072-IGQ6i1BPORUoDfQAUVUfZg7NDEDtwM3DcM2wSr6h"
access_secret = "UsoE76u5nKrptRR4E0hpiMc9vZ7wZ3kzVSxfzhKuuTvmY"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

search_terms = ['bitcoin', 'ethereum', 'dogecoin', 'shiva', 'XRP']


def stream_tweets(search_term):
    data = []
    counter = 0

    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=100, lang='es', tweet_mode='extended').items():
        tweet_details = {}
        tweet_details['name'] = tweet.user.screen_name
        tweet_details['tweet'] = tweet.full_text
        tweet_details['retweets'] = tweet.retweet_count
        tweet_details['location'] = tweet.user.location
        tweet_details['created'] = tweet.created_at.strftime("%d-%b-%Y")
        tweet_details['followers'] = tweet.user.followers_count
        tweet_details['is_user_verified'] = tweet.user.verified

        data.append(tweet_details)

        counter += 1
        if counter == 1000:
            break
        else:
            pass
    with open('data/{}.json'.format(search_term), 'w') as f:
        json.dump(data, f)
    print('saved file !')


if __name__ == "__main__":
    print('Starting...')
    for search_term in search_terms:
        stream_tweets(search_term)
    print('finished!')
