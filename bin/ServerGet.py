import urllib2

import threading
import json
import time
global lnglat
lnglat =[]

datefile = '../data'
mutex = threading.Lock()
class GetThread(threading.Thread):
    def __init__(self, id, name, counter):
        threading.Thread.__init__(self)
        self.threadId = id
        self.name = name
        self.couter = counter

    def getPoints(self):
        if mutex.acquire(1):
            global lnglat
            point = []
            if not lnglat:
                mutex.release()
                return None
            if len(lnglat) > 90:
                point.extend(lnglat[0: 90])
                del lnglat[0: 90]
            else:
                point.extend(lnglat)
                lnglat = None
            mutex.release()

        return point

    def run(self):
        num = 0
        data = ''
        i = 0
        while i < 10000:
            point = self.getPoints()
            if not point:
                print 'break---------------------'
                break
            else:
                num = num + len(point)
                time.sleep(1)

                URL = 'http://api.map.baidu.com/geoconv/v1/?coords='
                for i in range(0,len(point)):
                    if i == 0:
                        URL = URL + str(point[i]['x']) + ',' + str(point[i]['y'])
                    else:
                        URL = URL + ';' + str(point[i]['x']) + ',' + str(point[i]['y'])
                URL = URL + '&from=1&to=5&ak=21684640c3af3b7c4cb6fcc43906a4a3'

                req = urllib2.Request(URL)
                res = urllib2.urlopen( req )
                result = res.read()
                decodejson = json.loads(result)
                print str(self.threadId) + ' status :' + str(decodejson['status'])
                for u in decodejson['result']:
                    data = data + str(u['x']) + ' ' + str(u['y']) + '\n'
                res.close()

                continue
        try:
            file_object = open(datefile + '/outfile' + str(self.threadId), 'w')
            file_object.write(data)

        finally:
            file_object.close()
        print str(self.threadId) + ':' + str(num)

file_object = open(datefile + '/file_object.txt')
try:
    while True:
        text = file_object.readline()
        if not text:
            break
        text = text.strip().split(' ')
        if len(text) == 2:
            point = {}
            point['x'] = text[0]
            point['y'] = text[1]
            lnglat.append(point)


finally:
     file_object.close( )








thread1 = GetThread(1, 'getname', 1)
thread2 = GetThread(2, 'getname', 2)
thread3 = GetThread(3, 'getname', 3)
thread1.start()
thread2.start()
thread3.start()
