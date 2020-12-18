class average():
    def __init__(self,maxVal = 5):
        self.buf = []
        self.maxVal = maxVal

    def addVal(self,val):
        if len(self.buf) >= self.maxVal:
            self.buf.pop(0) # erstes element entfernen

        self.buf.append(val) # neues element hinten dran

    def getMean(self):
        return sum(self.buf) / len(self.buf)

    def get(self,val): # adds new value and gets new mean
        self.addVal(val)
        print(self.buf)
        return self.getMean()
