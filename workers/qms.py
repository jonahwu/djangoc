
import jieba
import libcorpus
import json
import requests

jieba.enable_parallel(2)
topKnum=20
apiurl='http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv'
headers = {'Content-type': 'application/json'}
#request.POST('http://116.62.136.201:100/sQMS_Production_MESws_STD/wsInvoke.asmx/invokeSrv')
#r = requests.request("POST", apiurl, headers=headers)
foo = {"method":"tcQMS.clsFMEALA.pharse_info_get","parameters":["{}"]}
json_data = json.dumps(foo)
r = requests.post(apiurl, headers=headers, data=json_data)
allPhrase = libcorpus.getAllPhrase(r)

#k=extractKeywords(types='intersection')
k=libcorpus.extractKeywords()
print('----extract result:----------')
print(k)
