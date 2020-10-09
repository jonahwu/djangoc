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
"""
jieba.enable_parallel(2)
topKnum=20
apiurl='http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv'
headers = {'Content-type': 'application/json'}
#request.POST('http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv')
#r = requests.request("POST", apiurl, headers=headers)
foo = {"method":"tcQMS.clsFMEALA.pharse_info_get","parameters":["{}"]}
json_data = json.dumps(foo)
r = requests.post(apiurl, headers=headers, data=json_data)
allPhrase = getAllPhrase(r)

#k=extractKeywords(types='intersection')
k=extractKeywords()
print('----extract result:----------')
print(k)

print(' --- token ----')

getNVCount(allPhrase)


SendBack(k)
"""

#tt=jieba.cut(allPhrase, cut_all=True, HMM=True)
#stopPhrase = movestopwords(allPhrase)

#re.sub(r'[\r\n][\r\n]{2,}', '\n\n', sourceFileContents)
#stopPhrase = re.sub(r'\n+(?=\n)', '\n', stopPhrase)

#stopPhrase = re.sub(r'[\r\n][\r\n]{2,}', '\n\n', stopPhrase)
#print(stopPhrase)

#seg_list =jieba.cut(stopPhrase)
#for seg1 in seg_list:
#    if len(seg1)!=0:
#        print(seg1)
#print("".join(seg_list))

#seg_list=jieba..Tokenizer()
#for seg in seg_list:
#    print(seg)
#print(len(seg_list))
#print(seg_list)





# parse from standard DH parser
"""
print(r)
rj=r.json()
rjj=json.loads(rj['d'])
rjjj=rjj['ResultJson']
rjjjj=json.loads(rjj['ResultJson'])
for i in rjjjj['pharse_detail']:
    print(i)
    print(i['pharse_type'],i['pharse_description'],i['pharse_stage'])
"""

# parse from standard


#print(rj['d']['Code'])

"""
print('---- clean -----')
rt=str(r.text)
rt=rt.replace('\\r\\n', '')
rt=rt.replace('\\', '')
rt=rt.replace('\"', '\'')
print(rt)
print('---- parse -----')
jrt=json.loads(rt)
print(jrt)

print('---- convert -----')
d = json.loads(r.text)
print(d)
"""


"""
#conn = http.client.HTTPSConnection('http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv')
conn = http.client.HTTPSConnection(host='http://116.62.136.201:100', port = 100)

headers = {'Content-type': 'application/json'}

#foo = {'text': 'Hello HTTP #1 **cool**, and #1!'}
foo = {"method":"tcQMS.clsFMEALA.pharse_info_get","parameters":["{}"]}
json_data = json.dumps(foo)

conn.request('POST', '/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv', json_data, headers)

response = conn.getresponse()
print(response.read().decode())
"""