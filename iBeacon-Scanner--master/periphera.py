from bluepy.bluepy.btle import Scanner, DefaultDelegate, Peripheral,UUID
from gi.repository import GObject

from gi.repository import Gtk,GLib

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        print("some")


def doCycle(per):
    
    print("sto girando")
    #suuid=UUID("uuid19b10000-e8f2-537e-4f6c-d104768a1214")
    #c=per.getServiceByUUID("19b10000-e8f2-537e-4f6c-d104768a1214").getCharacteristics()
    c=per.getServices()
    for cc in c:
            print ("serv. uuid"+cc.uuid.getCommonName())
            if cc.uuid.getCommonName()=="19b10000-e8f2-537e-4f6c-d104768a1214":
                print("trovato il servizio")    
                ccc=cc.getCharacteristics()
                for cccc in ccc:
                    print("char. uuid"+ cccc.uuid.getCommonName())
                    print("char. value"+str(cccc.read()))
            #per.disconnect()
    return True        
def startCycle():
    print ("cerco di connettermi")
    per=Peripheral("d7:84:e7:e2:87:68")
    per.setDelegate( MyDelegate() )
    print("connessione avvenuta")
    GObject.timeout_add(7000,doCycle,per)
    

startCycle()
Gtk.main()
