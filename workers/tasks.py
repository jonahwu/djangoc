import time
from celery import Celery
import os
p = os.path.abspath('..')
from qms.celery import app
import pickle
import jieba
from workers import libcorpus
import json
import requests
from celery import current_task


#broker = 'redis://127.0.0.1:6379'
#backend = 'redis://127.0.0.1:6379/0'

#app = Celery('my_task', broker=broker, backend=backend)


@app.task
def getdata(x, y):
    time.sleep(5)     # 模拟耗时操作
    filename='./cache/data.pkl'
    data = libcorpus.readPickle(filename)
    #data={'msg':'hello'}
    return data
    #return x + y

@app.task
def add(x, y):
    time.sleep(5)     # 模拟耗时操作

    data = {'k1':x, 'k2':y}
    filename='./cache/data.pkl'
    libcorpus.storePickle(data, filename )
    return x + y

@app.task
def getKeywords(kid, topKnum):
    #jieba.enable_parallel(2)
    #topKnum=20
    print(kid, topKnum)
    current_task.update_state(state='query api')
    apiurl='http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv'
    headers = {'Content-type': 'application/json'}
    #request.POST('http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv')
    #r = requests.request("POST", apiurl, headers=headers)
    foo = {"method":"tcQMS.clsFMEALA.pharse_info_get","parameters":["{}"]}
    json_data = json.dumps(foo)
    r = requests.post(apiurl, headers=headers, data=json_data)
    allPhrase = libcorpus.getAllPhrase(r)

    #k=extractKeywords(types='intersection')
    current_task.update_state(state='EXTRACT Keyword')
    k=libcorpus.extractKeywords(allPhrase=allPhrase)
    print('----extract result:----------')
    print(k)
    jsondata= {}
    jsondata['k']=k
    #filename='./cache/data.pkl'
    current_task.update_state(state='store data')
    filename='./cache/'+kid+'.pkl'
    libcorpus.storePickle(jsondata, filename )
    return kid
    #return jsondata

