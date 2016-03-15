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

tags = {}
users = {}
DUMP_TAGS = 1000
tags_count = 0

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):


    def __init__(self):
        self.count = 0;

    def on_data(self, data):

        global tags, users, DUMP_TAGS, tags_count

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

        if data['user'] not in users:
            users[data['user']] = len(users)

        if 'entities' in filt:
            if 'hashtags' in filt['entities']:
                for hashtag in filt['entities']['hashtags']:
                    h = hashtag['text']
                    if h not in tags:
			                     tags[h] = []
                    tags_count += 1
                    p = {}
                    p["user"] = users[data['user']]
                    p["date"] = data['date']
                    tags[h].append(p)
            if 'user_mentions' in filt['entities']:
                for mentioned in filt['entities']['user_mentions']:
                    x = mentioned['screen_name']
                    if x not in users:
                        users[x] = len(users)
                    print users[x], users[data['user']]

        if 'geo' in filt:
            data['coords'] = filt['geo']
        if 'text' in filt:
            data['text'] = filt['text']

        if tags_count > DUMP_TAGS:
			f = open('hashtags', 'w+')
			f.write(json.dumps(tags))
			f.close()
			DUMP_TAGS += 1000

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
            continue

try:
    sys.stdout.close()
except:
    pass
try:
    sys.stderr.close()
except:
    pass
