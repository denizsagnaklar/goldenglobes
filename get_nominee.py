import re
import os
import json
import collections
from filter_tweets import word_list

awardNames = [
"Best Motion Picture Drama",
"Best Motion Picture - Musical or Comedy",
"Best Director",
"Best Actor - Motion Picture Drama",
"Best Actor - Motion Picture Musical or Comedy",
"Best Actress - Motion Picture Drama",
"Best Actress - Motion Picture Musical or Comedy",
"Best Supporting Actor - Motion Picture",
"Best Supporting Actress - Motion Picture",
"Best Screenplay",
"Best Original Score",
"Best Original Song",
"Best Foreign Language Film",
"Best Animated Feature Film",
"Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures",
"Best Drama Series",
"Best Comedy Series",
"Best Actor in a Television Drama Series",
"Best Actor in a Television Comedy Series",
"Best Actress in a Television Drama Series",
"Best Actress in a Television Comedy Series",
"Best Limited Series or Motion Picture made for Television",
"Best Actor in a Limited Series or Motion Picture made for Television",
"Best Actress in a Limited Series or Motion Picture made for Television",
"Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television",
"Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television"]
def mostMatchAward(tweet):
    t = tweet.split(' ')
    mostMatch = 0
    mostAward = ""
    words = [re.sub(r'[\@|\:|\-|\"|\"|\'|\#|\.|\,]', '', word).capitalize() for word in t]
    if 'Best' not in words:
        return mostAward
    for award in awardNames:
        aw = award.split(' ')
        cnt = 0
        flimited = False
        cntlimited = False
        if 'Limited' in aw:
            flimited = True
        for word in words:
            if word in aw:
                cnt += 1
            if flimited and word == 'Limited':
                cntlimited = True
        if flimited and cntlimited:
            if cnt > mostMatch:
                mostMatch = cnt
                mostAward = award
            elif cnt == mostMatch:
                if len(award) < len(mostAward):
                    mostAward = award
            continue
        if cnt == mostMatch:
            if len(award) < len(mostAward):
                mostAward = award
        elif cnt > mostMatch:
            mostMatch = cnt
            mostAward = award
    return mostAward

notNomineeWords = ['Oh', 'LOL', 'As', 'as', 'A', 'a', 'And', 'and', 'But', 'but', 'THE', 'The', 'the', 'am', 'are', 'is', 'Am', 'Are', 'Is', 'You', 'You\'re', 'you', 'Im', 'I\'m', 'Me', 'me', 'We', 'we', 'Our', 'our', 'Us', 'us', 'Male', 'Female', 'Mexican', 'Man', 'Men', 'Womam', 'Women', 'He', 'Hes', 'he', 'She', 'Shes', 'she', 'I', 'It', 'it', 'its', 'Its', 'They', 'they', 'Why', 'why', 'Because', 'ReasonsWhy', 'Folks', 'A Lesbian', 'Please', 'Written', 'Look', 'How', 'how', 'When', 'when', 'Where', 'where', 'Here', 'here', 'There', 'there', 'Should', 'At', 'On', 'In', 'Just', 'just', 'GoldenGlobes', 'goldenglobes', 'Gay', 'No', 'no', 'None', 'none', 'Good', 'good', 'get', 'GetOut', 'GetIn', 'If', 'if', 'This', 'this', 'That', 'that', 'These', 'these', 'Those', 'those', 'Best', 'best', 'Maybe', 'May not', 'Tonight', 'Directors', 'Picture', 'All', 'all', 'Still', 'still', 'Reminder']

resultDict = {}
def findNominee(line):
    patterns = [r'nomin(.*)Best', r'Best(.*)nominee']
    for p in patterns:
        line = re.sub(r'RT', '', line)
        matchstr = re.findall(p ,line)
        if matchstr:
            (award, nominee) = extractNominee(line)
            award = mostMatchAward(award)
            if award not in resultDict:
                resultDict[award] = set([])
            if re.search(r'Dir.*', award):
                if re.search(r'Get.*', nominee):
                    continue
            if award in resultDict:
                if len(nominee) > 1 and nominee not in notNomineeWords:
                    t = nominee.split(' ')
                    s = t
                    for word in t:
                        if word in notNomineeWords:
                            s.remove(word)
                    nominee = ' '.join(s)
                    if len(nominee) > 1 and nominee not in notNomineeWords:
                        resultDict[award].add(nominee)

def extractNominee(text):
    sents = re.split(r'[:.!?]+',text)
    nominee = ''
    award = ''
    for s in sents:
        matchstr = re.search(r'(.*)nominated.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if matchstr:
            nominee = findNomineeName(matchstr.group(1))
            award = matchstr.group(2)

        matchstr = re.search(r'(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)nominee [#@]*([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if matchstr:
            award = matchstr.group(1)
            nominee = matchstr.group(2)

        matchstr = re.search(r'presents(.*)(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*).*nominee', s)
        if matchstr:
            nominee = findNomineeName(matchstr.group(1))
            award = matchstr.group(2)

        matchstr = re.search(r'introduc[es|ed|ing|e]+(.*)as.*nominee[s]*.*(Best ((?<!@#)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*))', s)
        if matchstr:
            nominee = matchstr.group(1)
            award = matchstr.group(2)

        matchstr = re.search(r'introduc[ing|es|ed|e]+(.*)nominated.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if matchstr:
            nominee = findNomineeName(matchstr.group(1))
            award = matchstr.group(2)

        matchstr = re.search(r'(.*)nominated for.*includ.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if matchstr:
            nominee = findNomineeName(matchstr.group(1))
            award = matchstr.group(2)

    award = award.rstrip(' ').lstrip(' ')
    nominee = nominee.rstrip(' ').lstrip(' ')
    nominee = nominee.lstrip('@')
    return (award, nominee)

def findNomineeName(text):
    nominee = ''
    m = re.search(r'([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', text)
    if m:
        nominee = m.group(1)
    else:
        m = re.search(r'([@#]\w+)', text)
        if m:
            nominee = m.group(1)

    return nominee

def output(dic):
    dic = collections.OrderedDict(sorted(dic.items()))
    # fn = open('nomineeResult.txt','w')
    for award in dic:
        if award == '':
            continue
        if len(dic[award]) == 0:
            continue
        print "Category: {}".format(award)
        print "Nominees: {}".format(', '.join(dic[award]))
        print "\t"

# with open("gg2018.json", 'r') as handle:
#     tweets = json.load(handle)
# open(str("nomin.txt"), 'w').write(str(word_list('nomin', tweets)))
# f = open(str('nomin.txt'), 'r')
# t = f.read()

# t = str(word_list("nomin"))
def get_nominee():
    tweets = word_list('nomin')

    for tweet in tweets:
        findNominee(tweet)
    output(resultDict)

