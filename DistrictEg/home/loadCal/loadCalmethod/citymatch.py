import pandas as pd

def getRegionSearchdf(region):
    search_df_file = region + ".pickle"
    search_df = pd.read_pickle(search_df_file)
    return search_df

def getSearchlib(city,buildtype):
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
    buildtype_dict = {
        '住宅建筑':'resident',
        '办公建筑':'office',
        '商业建筑':'shopping'
    }
    default_item = 'invalid choice'
    city_choice = city_dict.get(city,default_item)
    buildtype_choice = buildtype_dict.get(buildtype,default_item)
    return city_choice,buildtype_choice