import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pandas as pd
# from loadCal.knnSearch.districtloadsprediction import *
# from loadCal.knnSearch.mysql import *
from datetime import datetime
from loadCal.loadCalmethod.mongod import *
from loadCal.loadCalmethod.citymatch import *
from loadCal.loadCalmethod.knnSearch import *
import numpy as np
import os

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def CalLoads(request):
    if request.method == 'POST':
        requestData = request.body
        requestDict = json.loads(requestData.decode('utf-8'))
        # requestDict = json.loads(requestData)
        city = requestDict["city"]
        region = requestDict["region"]
        clRange = requestDict["cldateRange"]
        htRange = requestDict["htdateRange"]

        mongodDB = mongoConnection('mongodb://47.92.29.130:27017/','districtloads','jmlj','jmlj')
        
        

        date_col = mongodDB['DateTime']
        date_df = pd.DataFrame(list(date_col.find({},{'_id':0}))[0])
        date_str = date_df.replace('24:00:00', '00:00:00', regex=True)
        date = date_str['DateTime'].map(lambda x: datetime.strptime(x.strip(),'%m/%d  %H:%M:%S'))
        # date_lst = date.map(lambda x: str(x.month)+'-'+str(x.day)+' '+str(x.hour)).tolist()
        date_lst = [datetime.strftime(x,"%Y-%m-%d %H:%M:%S") for x in date.to_list()]


        cl_start = datetime.strptime(clRange[0], '%Y-%m-%d')
        cl_end =  datetime.strptime(clRange[1], '%Y-%m-%d')
        ht_start =  datetime.strptime(htRange[0], '%Y-%m-%d')
        ht_end =  datetime.strptime(htRange[1], '%Y-%m-%d')

        cldateRange = [[cl_start.month,cl_start.day],[cl_end.month,cl_end.day]]
        htdateRange = [[ht_start.month,ht_start.day],[ht_end.month,ht_end.day]]

        loads_dict = {"Date":date_lst,'resultData':{}}
        params_dict = requestDict['paramsDict']

        for item in params_dict:
            buildtype = item['buildtype']
            city_choice,buildtype_choice = getSearchlib(city,buildtype)
            lib_name = city_choice + buildtype_choice
            search_lib = file_path = os.getcwd() + "\\loadCal\\searchlib\\" + region + buildtype_choice + ".pickle"
            search_lib = pd.read_pickle(file_path)

            params = item['params']
            area = float(params['area'])
            params.pop('area')

            instance = [float(x) for x in list(params.values())]
            myclient = mongodDB[lib_name]
            x = neighber_search(instance,search_lib,'eu')
            y = loads_predict(area,x,myclient,date,cldateRange,htdateRange,'eu')
            title = item["title"]
            loads_dict['resultData'].update({title:y})

        preLocalDictJson = json.dumps(loads_dict,skipkeys=True, ensure_ascii=False)
        return JsonResponse(preLocalDictJson,safe=False)




