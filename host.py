import nltk
from nltk import *
from nltk.tokenize import TweetTokenizer
from nltk.probability import ConditionalFreqDist
from nltk.collocations import *
import re


with open('Word_List_Folder/monologue.txt', 'r') as myfile2:
	htweets = (myfile2.read().split('\', \'' or '\', \"' or '\", \"'))

hostTokens = []
nnps = []

tokenizer = TweetTokenizer(strip_handles=True)

'''for i in htweets:
	hostTokens.append(tokenizer.tokenize(i))'''

for i in htweets:
	hostTokens.append(nltk.pos_tag(tokenizer.tokenize(i)))


flatTokens = [item for sublist in hostTokens for item in sublist]

def getall(my_list, s): 
	return [x for x, y in my_list if y==s]

for i in hostTokens:
	nnps.append(getall(i, 'NNP'))

nnps =[item for sublist in nnps for item in sublist]
tokensClean =[i for i in nnps if not ('@' in i or 'GoldenGlobes' in i or 'Globes75' in i or 'RT' in i or 'Anniversary' in i or
	'Hollywood' in i or 'Hmm' in i or 'Globes' in i or 'Golden' in i or 'Wow' in i or ',' in i or '"' in i or 'RT' in i or ':' in i 
	or 'monologue' in i or 'and' in i or 'Weinstein' in i or 'Harvey' in i or 'Problem' in i)]


'''tokensClean =[i for i in flatTokens if not ('@' in i or 'GoldenGlobes' in i or 'Globes75' in i or 'RT' in i or 'Anniversary' in i or
	'Hollywood' in i or 'Hmm' in i or 'Globes' in i or 'Golden' in i or 'Wow' in i or ',' in i or '"' in i or 'RT' in i or ':' in i 
	or 'monologue' in i or 'and' in i)]'''

bgs = nltk.bigrams(tokensClean)
fdist = nltk.FreqDist(bgs)
hp = []
hostRaw = fdist.most_common(4)

nameCheck =[x[0] for x in hostRaw]
newCheck = []
for x, y in nameCheck:
	newCheck.append(x)
	newCheck.append(y)

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]
newCheck = unique(newCheck)

freqCheck =[x[1] for x in hostRaw]
print newCheck
a = float(freqCheck[2])
b = float(freqCheck[0])
c = a / b
if (c < 0.6):
	hp.append(newCheck[0])
	hp.append(newCheck[1])
else:
	hp.append(newCheck[0])
	hp.append(newCheck[1])
	hp.append(newCheck[2])
	hp.append(newCheck[3])

hp = ' '.join(hp)

print "Host(s): {}".format(hp)
