from django.shortcuts import render
from django.http import JsonResponse
import time
from workers.tasks import add
from workers.tasks import getdata
import celery
from celery import uuid






def simple_slow(request):
    #add.delay(2, 8)
    task_id = uuid()
    add.apply_async(args=[3, 7], expires=10, task_id=task_id)
    result = celery.result.AsyncResult(task_id)
    print(result.task_id)
    time.sleep(1)
    counter=0
    while True:
        print(result.status)
        time.sleep(1)
        if result.status=="SUCCESS":
            counter = counter + 1
            if counter >=3:
                break;
    response={'msg':"hello"}
    return JsonResponse(response)

def queryData(request):
    #add.delay(2, 8)
    task_id = uuid()
    #result = getData.apply_async(args=[3, 7], expires=10, task_id=task_id)
    result = getdata.apply_async(args=[3, 7], expires=10, task_id=task_id)
    result = celery.result.AsyncResult(task_id)
    print(result.task_id)
    time.sleep(1)
    counter=0
    while True:
        print(result.status)
        time.sleep(1)
        if result.status=="SUCCESS":
            counter = counter + 1
            if counter >=3:
                break;
    print('------ result collection -----')
    #print(result.info)
    keyword=result.info
    print(keyword)
    response=keyword

    #response={}
    #response={'msg':"hello"}
    return JsonResponse(response)

def syncbuild(request):
    bestModel="svm"
    s="1"
    o="1"
    d="1"
    rpn="1"

    response = {
        'msg':'best model: %s \n s:%s  o:%s  d:%s  rpn:%s '%(bestModel, s, o, d, rpn), # response message
                's': s,
                'o': o,
                'd': d,
                'rpn': rpn,
                'bestmodel': bestModel,
    }
    return JsonResponse(response) # return response as JSON

