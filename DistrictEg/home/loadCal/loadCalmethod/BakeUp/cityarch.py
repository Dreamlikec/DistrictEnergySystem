def get_city(prediction_point):
    #得到预测点的城市和建筑类型
    city = prediction_point[0]
    
    city_dict = {
        '北京': 'bj',
        '深圳': 'sz',
        '上海': 'sh',
        '武汉': 'wh',
        '长沙': 'cs',
        '南京': 'nj',
        '临沂': 'ly',
        '徐州': 'xz',
        '青岛': 'qd',
    }

    default_item = 'invalid choice'
    city_choice = city_dict.get(city,default_item)
    return city_choice

def get_archtype(prediction_point):
    arch_type = prediction_point[1]
    arch_dict = {
        '办公建筑':'office',
        '酒店建筑':'hotel',
        '住宅建筑':'resident',
        '医院建筑':'hospital',
        '学校建筑':'school',
        '商业建筑':'shopping',
    }
    default_item = 'invalid choice'
    arch_choice = arch_dict.get(arch_type,default_item)
    return arch_choice

def get_cityindex(prediction_point):
    #获得预测点所在的城市
    city = prediction_point[0]
    #得到预测城市需要的三项指标，分别为tlw,tlf,si,打包为一个city_index_dict字典
    city_index_dict = {
        '北京': [8.6,7.2,151.5],
        '深圳': [9,7.5,128.5],
        '上海': [9.4,8,131.3],
        '武汉': [11.4,9.2,129.2],
        '长沙': [11.4,9.8,132.1],
        '南京': [11.4,9,135.6],
        '临沂': [11,9.6,131.8],
        '徐州': [11,9.6,131.8],
        '青岛': [10.6,8,145.9],
    }
    
    default_item = 'invalid_item'
    city_index = city_index_dict.get(city,default_item)
    return city_index

def get_ClimaticRegion(prediction_point):
    #获得预测点所在的城市
    city = prediction_point[0]
    #获取预测点的建筑类型
    archType = prediction_point[1]
    #气候分区的字典
    city_climate_dict = {
        '北京': 'coldarea',
        '深圳': 'hotsummerwarmwinter',
        '上海': 'hotsummercoldwinter',
        '武汉': 'hotsummercoldwinter',
        '长沙': 'hotsummercoldwinter',
        '南京': 'hotsummercoldwinter',
        '临沂': 'coldarea',
        '徐州': 'coldarea',
        '青岛': 'coldarea',
    }
    default_item = 'invalid_region'
    climatic_region = city_climate_dict.get(city,default_item)
    return climatic_region