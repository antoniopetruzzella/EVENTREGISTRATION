import urllib.request
import json
RemoteDeviceId=1
urlGetSerial = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getserial'
urlGetStatus = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getstatus&RemoteDeviceId='+str(RemoteDeviceId)

def getResponse(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

visitModeOn=True
try:
    while visitModeOn:
        print(urlGetStatus)
        res = getResponse(urlGetStatus)
        cont = json.loads(res.decode('utf-8'))
        counter = 0
        for item in cont:
            counter += 1
            visitModeOn=int(item["ModeVisitOn"])
            print(visitModeOn)
        
except KeyboardInterrupt:
    exit()


