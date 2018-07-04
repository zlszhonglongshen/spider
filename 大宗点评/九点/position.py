# coding: utf-8
# 解析大众点评地图坐标参数(POI)

def to_base36(value):
    """将10进制整数转换为36进制字符串
    """
    if not isinstance(value, int):
        raise(TypeError("expected int, got %s: %r" % (value.__class__.__name__, value)))

    if value == 0:
        return "0"

    if value < 0:
        sign = "-"
        value = -value
    else:
        sign = ""

    result = []

    while value:
        (value, mod)= divmod(value, 36)
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])

    return(sign + "".join(reversed(result)))

def getPosition(C):
    """解析大众点评POI参数
    """
    digi = 16
    add = 10
    plus = 7
    cha = 36
    I = -1
    H = 0
    B = ''
    J = len(C)
    G = ord(C[-1])
    C = C[:-1]
    J -= 1
    
    for E in range(J):
        D = int(C[E], cha) - add
        if D >= add:
            D = D - plus
        B += to_base36(D)
        if D > H:
            I = E
            H = D

    A = int(B[:I], digi)
    F = int(B[I+1:], digi)
    L = (A + F - int(G)) / 2
    latitude = float(F - L) / 100000
    longitude = float(L) / 100000
    return longitude,latitude

if __name__ == '__main__':
    (longitude,latitude)=getPosition('IJGDHFZVIBRDHR')
    print("longitude:%s°E,latitude:%s°N"%(longitude,latitude))