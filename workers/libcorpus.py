import http.client
import json
import requests
import jieba.analyse
from nltk.corpus import stopwords
import nltk
import re
import jieba.posseg as pseg
import pickle

def storePickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    f.close()
    return

def readPickle(filename):
    data = ""
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    f.close()
    return data

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def movestopwords(sentence):
    stopwords = stopwordslist('./workers/stop_words.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t'and'\n':
                outstr += word
                # outstr += " "
    return outstr

def getNVCount(text):

    print('--- pseg -----')
    #jieba.enable_paddle()
    words = pseg.cut(allPhrase)
    counter = 0
    for word, flag in words:
        if flag != "x":
            #print('%s %s' % (word, flag))
            counter = counter + 1
    print(' total counter is:', counter)
    # can not use cut since no 詞性, and with lots of blank after cut"
    """
    counterj=0
    dd = jieba.cut(allPhrase)
    for word in dd:
            print('%s' % (word))
            counterj = counterj + 1
    print(counterj)
    """


    return counter

def getAllPhrase(r):
    print('----- input data ------')
    print(r)
    print('----- ------')
    rj=r.json()
    rjj=json.loads(rj['d'])
    rjjj=rjj['ResultJson']
    rjjjj=json.loads(rjj['ResultJson'])
    allPhrase=""
    for i in rjjjj['pharse_detail']:
        print(i)
        print(i['pharse_type'],i['pharse_description'],i['pharse_stage'])
        allPhrase=allPhrase+i['pharse_description']+' '

    allPhrase = movestopwords(allPhrase)
    print('------ clean phrase -------')
    print(allPhrase)
    return allPhrase

def getIntersection(k1, k2):
    retintsect = list(set(k1).intersection(set(k2)))
    return retintsect

def getAllPhraseNewX(r):
    #print(r)
    rj=r.json()
    print(rj)
    print('------- parse ----------')
    rjjjj=rj['d']['ResultJson']
    print('rjjjjjjj')
    print(rjjjj)
    #rjj=json.loads(rj['d'])
    #rjjj=rjj['ResultJson']
    #rjjjj=json.loads(rjj['ResultJson'])
    allPhrase=""
    for i in rjjjj['pharse_detail']:
        print(i)
        print(i['pharse_type'],i['pharse_description'],i['pharse_stage'])
        allPhrase=allPhrase+i['pharse_description']+' '

    return allPhrase


def readKeyworkdFromStored(tid):
    keyword = readPickle('./cache/'+tid+'.pkl')
    return keyword

def extractKeywords(allPhrase='', types='tfidf'):
    topKnum=20
    jieba.analyse.set_stop_words("./workers/stop_words.txt")
    #jieba.analyse.set_idf_path("./idf.txt.big")

    print('--- types:',types)
    if types=='tfidf' or types=='intersection':
        print('--- tfidf -----')
        keywords1=jieba.analyse.extract_tags(allPhrase,topK=topKnum, withWeight=False, allowPOS=('n', 'v', 'nr', 'nz', 'ns','LOC', 'ORG', 't', 'PER', 'eng'))
        #keywords1=jieba.analyse.extract_tags(allPhrase,topK=topKnum, withWeight=False)
        print(keywords1)
        if types=='tfidf':
            return keywords1
    if types=='textrank' or types=='intersection':
        print('--- textrank -----')
        keywords2 = jieba.analyse.textrank(allPhrase, topK=topKnum, withWeight=False, allowPOS=('n', 'v', 'nr', 'nz', 'ns','LOC', 'ORG', 't', 'PER', 'eng'))
        #keywords2 = jieba.analyse.textrank(allPhrase, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        print(keywords2)
        if types=='textrank':
            return keywords2
        return keywords2
    if types=='intersection':
        print(' ---- intersection -----')
        interKey= getIntersection(keywords1, keywords2)
        print(interKey)
        return interKey

def SendBack(k):
    jsondata= {}
    jsondata['k']=k
    jsonStr=json.dumps(jsondata)
    print(' --- show return result ----')
    print(jsonStr)
    #payload = {'some': 'data'}
    #headers = {'Content-type': 'application/json'}
    #response = requests.post(url, data=json.dumps(payload), headers=headers)

    return True
