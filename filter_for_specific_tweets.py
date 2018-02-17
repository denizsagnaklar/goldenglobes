# filter tweets

import re
import json
# import nltk
# from nltk.corpus import stopwords

url_pattern = r'http\S+'

# removes emojis
def remove_emojis(tweet_text):
    return tweet_text.encode('ascii', 'ignore')

# removes urls
def remove_urls(tweet_text):
    return re.sub(url_pattern, '', tweet_text, flags=re.IGNORECASE)

def word_list(keyword, tweets):
    new_list = []
    for tweet in tweets:
        text = tweet['text']
        s = re.search(keyword, text)
        if s is not None:
        	text = remove_emojis(remove_urls(text))
        	new_list.append(text)
    return new_list

with open("gg2018.json", 'r') as handle:
        tweets = json.load(handle)

print "json loaded"

keyword_list = ["win", "won", "nominee", "nominees", "host", "hosts", 
"award", "awards", "best", "performance", "announce", "introduce", "actor", 
"actress", "supporting", "role", "director", "screenplay", "motion", 
"picture", "drama", "comedy", "animated", "foreign", "original", "song", 
"television", "tv", "series", "musical", "limited", "cecil", "demille"]

def make_doc(keyword, tweets):
	open(str("Word_List_Folder/" + keyword + ".txt"), 'w').write(str(word_list(keyword, tweets)))

i = 0
for word in keyword_list:
	make_doc(word, tweets)
	print i
	i+=1


# RETURN SMALLER LIST

# smaller_list = []
# small_list  = open("small_json_list.txt", 'w')

# small_list.write('[')
# for i in range(0, 7500):
#     # smaller_list.append(tweets[i])
#     small_list.write(str(tweets[i]))
# small_list.write(']')
# print smaller_list


