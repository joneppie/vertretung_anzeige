import time
import os
import datetime

class Zeiten:

    def __init__(self,  path,  file='time.txt'):
        self.path = path
        self.file = file
        self.time = int(time.mktime(datetime.datetime.strptime("01.01.2000", "%d.%m.%Y").timetuple()))

    def writeTime(self):
        timefile = open(self.path + "/" + self.file, "w")
        timefile.write(str(int(time.time())))
        timefile.close()

    def readTime(self):
        if os.path.isfile(self.path + "/" + self.file):
            timefile = open(self.path + "/" + self.file, "r")
            timeStr = timefile.readline().rstrip()
            timefile.close()
            self.time = int(timeStr)
            return int(timeStr)
        else:
            return  int(time.mktime(datetime.datetime.strptime("01.01.2000", "%d.%m.%Y").timetuple()))

    def getTime(self):
        return self.time

    def getToday():
        return time.mktime(time.strptime(datetime.datetime.now().strftime("%d.%m.%Y"), "%d.%m.%Y"))
