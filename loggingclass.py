import datetime

class logging():
    def __init__(self,outputType = "mock",conf = {}):
        self.outputType = outputType
        self.config = conf
        self.DEBUG = False

    def log(self,value,name):
        print(name,":",value)
        if (self.outputType == "csv"):
            with open(self.config['outputFile'],"a+") as outFile:
                for val in self.config['format']:
                    outFile.write(str(value[val])+",")
                outFile.write("\n")
        
