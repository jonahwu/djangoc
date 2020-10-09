import time
from celery import Celery
import os
p = os.path.abspath('..')
from qms.celery import app
import pickle

#broker = 'redis://127.0.0.1:6379'
#backend = 'redis://127.0.0.1:6379/0'

#app = Celery('my_task', broker=broker, backend=backend)

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

@app.task
def getdata(x, y):
    time.sleep(5)     # 模拟耗时操作
    filename='./cache/data.pkl'
    data = readPickle(filename)
    #data={'msg':'hello'}
    return data
    #return x + y

@app.task
def add(x, y):
    time.sleep(5)     # 模拟耗时操作

    data = {'k1':x, 'k2':y}
    filename='./cache/data.pkl'
    storePickle(data, filename )
    return x + y



