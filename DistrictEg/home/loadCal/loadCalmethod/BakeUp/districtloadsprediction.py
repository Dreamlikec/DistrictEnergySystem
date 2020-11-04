import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from loadCal.knnSearch.distanceformula import *
from loadCal.knnSearch.cityarch import *
from loadCal.knnSearch.mysql import *
import json
import sys
import os,django
from django.http import JsonResponse, HttpResponse
import pandas.io.formats.excel

def neighbor_search(prediction_point,metric,n,mysqldb):
    ottv_sheet = get_ClimaticRegion(prediction_point)+get_archtype(prediction_point)
    print(ottv_sheet)
    #查询汇总表，可根据需要自行修改
    summary_rows = mysqldb.query("select * from "+ottv_sheet)
    #将汇总表的格式转化为Dataframe,并只读入从第2列开始后面的9列，其中第2列为OTTV值，我们需要比较的是OTTV值来判断建筑的相似性，同事删除shedule列
    summary_table = pd.DataFrame(list(summary_rows)).iloc[:,1:10].drop([8],axis = 1)
    #将建筑信息表进行归一化
    summary_table_nor = MinMaxScaler().fit_transform(summary_table)
    #得到建筑信息表中的最小值array和最大值array
    min_building_arr = pd.DataFrame.min(summary_table)
    max_building_arr = pd.DataFrame.max(summary_table)
    #prediction_point为设计人员提供的建筑信息列表（此列表中不包含城市和建筑类型），注：此列表不包含OTTV值，而应该通过计算得出
    #设计人员输入列表的顺序为 heding = ['城市','建筑类型','面积','建筑体形系数','夏季室内设定温度(℃)','冬季室内设定温度(℃)','室内人员密度(m2/p)','照明功率密度(W/m2)','设备功率密度(W/m2)','窗墙比','窗的太阳得热系数shgc','窗的传热系数(W/m2·℃)','墙的传热系数(W/m2·℃)']
    city_index = get_cityindex(prediction_point)
    tlw = city_index[0]
    tlf = city_index[1]
    si = city_index[2]
    #tlw为墙的平均温差，tlf为窗的平均传热温差，si为所在城市的平均日射负荷强度，这些值与所在城市有关
    ottv = (1-prediction_point[9])*prediction_point[12]*tlw+prediction_point[9]*prediction_point[11]*tlf+prediction_point[9]*prediction_point[10]/0.85*si
    #将ottv插入原来的预测列表中，并仅保存从建筑体形系数开始后的8项
    prediction_point_new = np.insert(prediction_point,4,values = ottv)[3:11].astype(np.float)
    #对于预测点我们也需要做归一化操作
    prediction_point_new_nor = (prediction_point_new - min_building_arr)/max_building_arr
    #设置一个distance ndarry用于保存预测点和5000个点的距离
    distance = np.ones(5000)
    #计算预测点和每个点的距离
    for i in range(5000):
        distance[i] = cal_distance(prediction_point_new_nor,summary_table_nor[i],'eudist')
    #将距离进行排序，并返回按小到大的排序序号和从小到大的距离，均选取前n项
    order_min_distance = np.argsort(distance)[0:4]
    min_distance = distance[order_min_distance]
    #将序号和距离合并成二维数组返回
    neighbor = np.concatenate((order_min_distance[:,np.newaxis],min_distance[:,np.newaxis]),axis = 1)
    return neighbor

def Loads_predict(prediction_point,neighbor,mysql):
    #获得mysql中的城市及建筑类型索引
    city_arch_type = get_city(prediction_point)+get_archtype(prediction_point)
    #得到建筑的空调面积
    area = prediction_point[2]
    #如果距离为0，直接将该表返回
    prediction = np.zeros(8760*2).reshape(8760,2)
    if (neighbor[0][1] == 0):
        rows = np.array(mysql.query("select * from {}".format(city_arch_type + str(int(neighbor[0][0])))))
        prediction[:,[0,1]] = rows[:,[1,2]] * area
    #如果距离不为0，则返回相近的n个点
    else:
        n = len(neighbor)
        #计算邻居的权重和总权重
        weight = []
        totalweight = 0
        for i in range(0,n):
            weight.append(1/neighbor[i][1])
        totalweight =sum(weight)
        #读取邻居的数据表np.zeros(8760*3).reshape(8760,3)
        for i in range(1,n):
            rows = np.array(mysql.query("select * from {}".format(city_arch_type+str(int(neighbor[i][0])))))
            #将列表的第2列和第3列乘以权重和面积
            prediction[:,[0,1]] += rows[:,[1,2]].astype(np.float) * weight[i] * area / totalweight

        date = rows[:,0].astype(np.str)
        prediction = np.around(prediction,decimals=2)
        # 将日期和结果竖向并列
        prediction = np.concatenate((date[:,np.newaxis], prediction),axis = 1)
    return prediction