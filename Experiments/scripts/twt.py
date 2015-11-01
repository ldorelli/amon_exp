#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys

#Variables that contains the user credentials to access Twitter API 
access_token = "132399683-R2FgZoNS8kgdUR8RAD9oVw3rT1dX32hlo10TLFgi"
access_token_secret = "uF4nRCaXkjnrAoMce85Xv0V3uXuFRM0HkFD0quWALjm19"
consumer_key = "KU24cYenLid8xP7h1hoZ7kFPc"
consumer_secret = "c1I5Ixn2fWfxeLzk1zTipkvFI1fJv8N0eDe7t9gMR63VvVCu76"

users = {}
MAX_USERS = 80000000

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self):
        self.count = 0;
    
    def on_data(self, data):
        filt = json.loads(data)

        data = {}
        if 'user' in filt:
            data['user'] = filt['user']['screen_name']
        else:
            return

        data['mentions'] = []
        data['hashtags'] = []
        if 'created_at' in filt:
            data['date'] = filt['created_at']
        


        l = len(users)
        if l < MAX_USERS and data['user'] not in users:
            users[data['user']] = l

        if 'entities' in filt:
            if 'hashtags' in filt['entities']:
                for hashtag in filt['entities']['hashtags']:
                    h = hashtag['text']
                    st = u'tags/' + h
                    f = open(st, 'a+')
                    # f.write(str(users[data['user']]))
                    f.close()

            if 'user_mentions' in filt['entities']:
                for mentioned in filt['entities']['user_mentions']:
                    x = mentioned['screen_name']
                    l = len(users)
                    if l < MAX_USERS and x not in users:
                        users[x] = l
                    if x in users and data['user'] in users:
                        print users[x], users[data['user']]

        if 'geo' in filt:
            data['coords'] = filt['geo']
        if 'text' in filt:
            data['text'] = filt['text']
        
        # if 'mentions' in data and 'hashtags' in data:
 	       # print json.dumps(data)
        # if 'retweeted_status' in filt and filt['retweeted_status']:
	       #   print json.dumps(data)
        return True

    def on_error(self, status):
    	print(status)


if __name__ == '__main__':

    while True:
        try:
            #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.sample()
        except KeyboardInterrupt:
			break
        except Exception,e:
            print str(e)
            continue

try:
    sys.stdout.close()
except:
    pass
try:
    sys.stderr.close()
except:
    pass
