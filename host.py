import nltk
from nltk import *
from nltk.tokenize import TweetTokenizer
from nltk.probability import ConditionalFreqDist
import re

'''with open('Word_List_Folder/host.txt', 'r') as myfile:
    htweets = myfile.read().split('\', \'' or '\', \"' or '\", \"')

with open('Word_List_Folder/hosts.txt', 'r') as myfile2:
	htweets2 = (myfile2.read().split('\', \'' or '\', \"' or '\", \"'))'''

with open('Word_List_Folder/monologue.txt', 'r') as myfile2:
	htweets = (myfile2.read().split('\', \'' or '\', \"' or '\", \"'))

'''for i in htweets2:
	htweets.append(i)

for i in htweets3:
	htweets.append(i)'''

hostTokens = []
nnps = []

tokenizer = TweetTokenizer(strip_handles=True)


for i in htweets:
	hostTokens.append(nltk.pos_tag(tokenizer.tokenize(i)))

def getall(my_list, s): 
	return [x for x, y in my_list if y==s]


for i in hostTokens:
	nnps.append(getall(i, 'NNP'))

nnps =[item for sublist in nnps for item in sublist]
nnps_clean =[i for i in nnps if not ('@' in i or 'GoldenGlobes' in i or 'Globes75' in i or 'RT' in i or 'Anniversary' in i or
	'Hollywood' in i or 'Hmm' in i or 'Globes' in i or 'Golden' in i or 'Wow' in i)]

fdist = FreqDist(nnps_clean)
hostRaw = fdist.most_common(4)
hostRaw = [x[0] for x in hostRaw]
hp = []
for i in hostRaw:
	hp.append(i)
hp = ' '.join(hp)

print "Host: {}".format(hp)




''''tokenizer = TweetTokenizer(strip_handles=True)
t = tokenizer.tokenize(tweet) '''

'''for i in hostTokens:
	if (re.findall(i)):
		print i'''
