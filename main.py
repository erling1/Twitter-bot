from dotenv import load_dotenv
import os
import tweepy

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')

Bearer_Token = os.getenv('BearerToken')

ACCESS_Token = os.getenv('AccesToken')
ACCESS_Secret = os.getenv('Secret')




# Function to extract tweets
def get_tweets(username):
         
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
 
        # Access to user's access key and access secret
        auth.set_access_token(Acces_Token, ACCES_Secret)
 
        # Calling api
        api = tweepy.API(auth)
 
        # 200 tweets to be extracted
        number_of_tweets=2
        tweets = api.user_timeline(screen_name=username)
 
        # Empty Array
        tmp=[] 
 
        # create array of tweet information: username, 
        # tweet id, date/time, text
        tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created 
        for j in tweets_for_csv:
 
            # Appending tweets to the empty array tmp
            tmp.append(j) 
 
        # Printing the tweets
        print(tmp)
 

def post_tweet(tweet: str):

    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_Token, ACCESS_Secret)
     
    api = tweepy.API(auth)
    api.update_status(tweet)


# Driver code
#if __name__ == '__main__':
 
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    #get_tweets("twitter-handle") 