
def convertColor(value, colorformat):
    if (colorformat == '888'):
        invalue = int(value) 
        value = [(invalue >> 16) & 255, (invalue >> 8) & 255, (invalue) & 255]

    elif (colorformat == 'hex'):
        value = [int(value[0:2],16), int(value[2:4],16), int(value[4:6],16)]
        
    return value

def convertColorTo(value, colorformat):
    #invalue = array(r,g,b)
    if (colorformat == '888'):
        retVal = (value[0] << 16) & 255 | (value[1] << 8) & 255 | (value[2]) & 255

    return str(retVal)


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

def normalizeColor(value,n = 255):
    normalized = [
        float(value[0]) / n,
        float(value[1]) / n,
        float(value[2]) / n
    ]
    maxValue = getMax(normalized)
    if (maxValue == 0):
        factor = 0
    else:
        factor = n / getMax(normalized)
    return [
        normalized[0] * factor,
        normalized[1] * factor,
        normalized[2] * factor
    ]

def dimColor(ratio,i,n):
    normalized = normalizeColor(ratio,n)
    return [
        normalized[0] * i / n,
        normalized[1] * i / n,
        normalized[2] * i / n
    ]
