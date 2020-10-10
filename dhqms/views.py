from django.shortcuts import render
from django.http import JsonResponse
import time
from workers.tasks import add
from workers.tasks import getdata
from workers.tasks import getKeywords
import celery
from celery import uuid
from workers import libcorpus
from celery.result import AsyncResult






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
    task_id = uuid()
    #result = getData.apply_async(args=[3, 7], expires=10, task_id=task_id)
    #result = extractKeywords.apply_async(args=[3, 7], expires=6000, task_id=task_id)
    result = getKeywords.apply_async(args=[task_id, 20], expires=6000, task_id=task_id)
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
    #keyword=result.info
    #print(keyword)
    tid=result.info
    keyword = libcorpus.readKeyworkdFromStored(tid)
    response= keyword
    # we can return data to DH by using rest post
    return JsonResponse(response) # return response as JSON


def getKeywordsByTaskID(request, tid):
    response = libcorpus.readKeyworkdFromStored(str(tid))
    return JsonResponse(response)

def getTaskIDStatus(request, tid):
    ret = libcorpus.getTaskIDStatus(str(tid))
    response = {}
    response['status']=ret
    return JsonResponse(response)
