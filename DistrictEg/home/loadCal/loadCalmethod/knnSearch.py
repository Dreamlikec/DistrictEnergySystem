import numpy as np
import pandas as pd
import operator
from datetime import datetime

def cal_distance(x,y):
    return (np.sum(np.square(x - y)))

def neighber_search(instance,search_df,metrics):
    distances = []
    max = search_df.max()
    min = search_df.min()

    df_norm = ((search_df - min) / (max - min)).values
    in_norm = ((instance - min) / (max - min)).values

    dis_min_value = 1000
    dis_submin_value = 1000
    dis_min_index = 0
    dis_submin_index = 0

    if metrics == 'eu':
        for i in range(len(df_norm)):
            distance = cal_distance(in_norm, df_norm[i])
            if distance < dis_min_value and distance!=0:
                dis_submin_value = dis_min_value
                dis_min_value = distance
                dis_submin_index = dis_min_index
                dis_min_index = i + 1
            elif distance == 0:
                dis_min_value = distance
                dis_min_index = i + 1
                break
        distances.append((dis_min_value,dis_min_index))
        distances.append((dis_submin_value,dis_submin_index))
    neighbors = []
    for i in range(2):
        neighbors.append(distances[i])
    return neighbors

def loads_predict(area,neighbors,build_col,date,cldateRange,htdateRange,metrics):
    distances = list(map(operator.itemgetter(0),neighbors))
    orders = list(map(operator.itemgetter(1),neighbors))
    totalweight = 0
    cllst_col = []
    htlst_col = []
    mhtlst_col = []

    cl_starttime = datetime(1900,cldateRange[0][0],cldateRange[0][1],0)
    cl_endtime = datetime(1900,cldateRange[1][0],cldateRange[1][1],0)
    ht_starttime = datetime(1900,htdateRange[0][0],htdateRange[0][1],0)
    ht_endtime = datetime(1900,htdateRange[1][0],htdateRange[1][1],0)

    cl_index = date[(date >= cl_starttime)&(date <= cl_endtime)].index
    ht_index = date[(date <= ht_endtime)|(date >= ht_starttime)].index

    date_index = list(date.index)
    non_cl_list = list(set(date_index).difference(set(cl_index)))
    non_ht_list = list(set(date_index).difference(set(ht_index)))

    if metrics =="eu":
        if distances[0] == 0:
            cllst_narr = np.array(list(list(build_col.find({'order':orders[0]},{'_id':0, 'cl':1}))[0].values())[0]) 
            for i in non_cl_list:
                cllst_narr[i] = 0
       
            htlst_narr = np.array(list(list(build_col.find({'order':orders[0]},{'_id':0, 'ht':1}))[0].values())[0]) 
            for i in non_ht_list:
                htlst_narr[i] = 0
            
            mhtlst_narr = np.array(list(list(build_col.find({'order':orders[0]},{'_id':0, 'mht':1}))[0].values())[0])
            for i in non_ht_list:
                mhtlst_narr[i] = 0

            cl_max = round(np.max(cllst_narr),2)
            ht_max = round(np.max(htlst_narr),2)
            mht_max = round(np.max(mhtlst_narr),2)

            ht_sum = round(np.sum(htlst_narr)/1000,2)
            cl_sum = round(np.sum(cllst_narr)/1000,2)
            mht_sum = round(np.sum(mhtlst_narr)/1000,2)

            clloads = round(cl_max *area,2)
            htloads = round(ht_max *area,2)

            cllst_lst = list(area * cllst_narr)
            htlst_lst = list(area * htlst_narr)
            mhtlst_lst = list(area * mhtlst_narr) 
            loads_dict = {"winter":{"value_list":htlst_lst,"maxindex":ht_max,"mmaxindex":mht_max,"htloads":htloads,"sum":ht_sum,"msum":mht_sum},"summer":{"value_list":cllst_lst,"maxindex":cl_max,"sum":cl_sum,"clloads":clloads}}
            return loads_dict        
        else:
            distances = np.array(distances)
            distances_reci = 1/distances
            totalweight = np.sum(distances_reci)
            weights = distances_reci/totalweight
            for i in range(len(orders)):
                cllst_i = np.array(list(list(build_col.find({'order':orders[i]},{'_id':0, 'cl':1}))[0].values())[0])
                for j in non_cl_list:
                    cllst_i[j] = 0
                htlst_i = np.array(list(list(build_col.find({'order':orders[i]},{'_id':0, 'ht':1}))[0].values())[0])
                for j in non_ht_list:
                    htlst_i[j] = 0
                mhtlst_i = np.array(list(list(build_col.find({'order':orders[i]},{'_id':0, 'mht':1}))[0].values())[0])
                for j in non_ht_list:
                    mhtlst_i[j] = 0
                cllst_col.append(cllst_i)
                htlst_col.append(htlst_i)
                mhtlst_col.append(mhtlst_i)


            cllst_narr = np.sum([weights[i]* cllst_col[i] for i in range(len(weights))],axis=0) 
            htlst_narr = np.sum([weights[i]* htlst_col[i] for i in range(len(weights))],axis=0) 
            mhtlst_narr = np.sum([weights[i]* mhtlst_col[i] for i in range(len(weights))],axis=0)
            cllst_lst = list(area * cllst_narr)
            htlst_lst = list(area * htlst_narr)
            mhtlst_lst = list(area * mhtlst_narr) 
            
            cl_max = round(np.max(cllst_narr),2)
            ht_max = round(np.max(htlst_narr),2)
            mht_max = round(np.max(mhtlst_narr),2)

            clloads = round(cl_max *area,2)
            htloads = round(ht_max *area,2)
            
            cl_sum = round(np.sum(cllst_narr,axis = 0) / 1000,2)
            ht_sum = round(np.sum(htlst_narr,axis = 0) / 1000,2)
            mht_sum = round(np.sum(mhtlst_narr,axis = 0) / 1000,2)

            loads_dict = {"winter":{"value_list":htlst_lst,"maxindex":ht_max,"mmaxindex":mht_max,"htloads":htloads,"sum":ht_sum,"msum":mht_sum},"summer":{"value_list":cllst_lst,"maxindex":cl_max,"sum":cl_sum,"clloads":clloads}}
            return loads_dict        

