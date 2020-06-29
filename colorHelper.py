
def convertColor(value, colorformat):
    if (colorformat == '888'):
        invalue = int(value) 
        value = [(invalue >> 16) & 255, (invalue >> 8) & 255, (invalue) & 255]

    elif (colorformat == 'hex'):
        value = [int(value[0:2],16), int(value[2:4],16), int(value[4:6],16)]
        
    return value

def dimCalculator(start, end, i, n):
    d = [
        end[0] - start[0],
        end[1] - start[1],
        end[2] - start[2]
    ]
    return [
        start[0] + d[0] * float(i) / n,
        start[1] + d[1] * float(i) / n,
        start[2] + d[2] * float(i) / n
    ]

def isMax(value,max):
    for v in value:
        if (v >= max):
            return True
    return False

def getMax(value):
    m = 0
    for v in value:
        if v >= m:
            m = v
    return m

def dimColor(ratio,i,n):
    normalized = [
        float(ratio[0]) / n,
        float(ratio[1]) / n,
        float(ratio[2]) / n
    ]
    factor = n / getMax(normalized)
    normalized = [
        normalized[0] * factor,
        normalized[1] * factor,
        normalized[2] * factor
    ]
    print("normalized:",normalized)
    return [
        normalized[0] * i / n,
        normalized[1] * i / n,
        normalized[2] * i / n
    ]