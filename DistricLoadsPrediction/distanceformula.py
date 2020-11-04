import numpy as np

def cal_distance(x, y, metric):
    #欧式距离计算公式
    def eudist(x,y):
        distance  = np.sqrt(np.sum(np.square(x-y)))
        return distance

    #街区距离计算公式
    def cityblock(x,y):
        distance = np.sum(abs(x - y))
        return distance

    #棋盘距离计算公式
    def chessboard(x,y):
        distance = max(abs(x-y))
        return distance

    #兰氏距离
    def lance(x,y):
        distance = np.sum(abs((x-y)/(x+Y)))
        return distance

    def linear(x,y):
        distance = 0
        distance = 0.35 * (cityblock(x,y) + chessboard(x,y))
    
    switch = {
        "eudist": lambda x, y: eudist(x, y),
        "cityblock": lambda x, y: cityblock(x, y),
        "chessboard": lambda x, y: chessboard(x, y),
        "lance": lambda x, y: lance(x, y),
        "linear": lambda x, y: linear(x, y)
    }
    try:
        distance = switch[metric](x,y)
    except KeyError as e:
        print("error")
    return distance
