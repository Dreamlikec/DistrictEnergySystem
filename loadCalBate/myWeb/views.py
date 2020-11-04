import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from myWeb.districtloadsprediction import *
from myWeb.mysql import *


def index(request):
    return render( request, 'index.html' )


def doCal(request):
    if request.method == 'POST':
        # print(request.POST)

        # 下面是ajax过来是json 的时候的取值
        # request_dict = json.loads(request.body.decode('utf-8'))
        # city = request_dict.get('city')

        # 下面是ajax过来是普通键值对文本时候的取值
        city = request.POST.get( 'city', None )
        jzlx = request.POST.get( 'jzlx', None )
        gnmj = float(request.POST.get( 'gnmj', None ))
        jztx = float(request.POST.get( 'jztx', None ))
        xjwd = float(request.POST.get( 'xjwd', None ))
        djwd = float(request.POST.get( 'djwd', None ))
        rymd = float(request.POST.get( 'rymd', None ))
        zmgl = float(request.POST.get( 'zmgl', None ))
        sbgl = float(request.POST.get( 'sbgl', None ))
        cqb = float(request.POST.get( 'cqb', None ))
        cdrxs = float(request.POST.get( 'cdrxs', None ))
        ccrxs = float(request.POST.get( 'ccrxs', None ))
        qcrxs = float(request.POST.get( 'qcrxs', None ))

    # 应该调用 KNN搜索算法了，此处省略 N行
    mysqldb = MySql( host="rm-8vbbe68p76ru6v950mo.mysql.zhangbei.rds.aliyuncs.com",
                     username="energyinstitute",
                     password="3edc$RFV",
                     port=3306,
                     database="district_loads_forecast" )
    # 生成一个测试点
    # test_point = []
    # test_point = ['北京', '酒店建筑', 100000, 0.1, 24, 20, 10, 12, 15, 0.4, 0.44, 1.5, 1]
    test_point = [city, jzlx, gnmj, jztx, xjwd, djwd, rymd, zmgl, sbgl, cqb, cdrxs, ccrxs, qcrxs]
    # 找到与其相似的4个邻近点
    neighbor = neighbor_search( test_point, "eudist", 4, mysqldb )
    # 做出负荷预测
    prediction_list = Loads_predict( test_point, neighbor, mysqldb )
    # 将mysql关闭
    mysqldb.close()
    # 计算结果按照拼接的json返回数据
    # 返回单个字符串时：
    re = prediction_list.tolist()
    reJson = json.dumps( re )
    return JsonResponse( reJson, safe=False )
