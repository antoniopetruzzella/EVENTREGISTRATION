# test BLE Scanning software
# jcs 6/8/2014
import time
import gi
    
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib
from bluepy.bluepy.btle import Scanner, DefaultDelegate, Peripheral
   
# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    #def handleDiscovery(self, dev, isNewDev, isNewData):
     #   if isNewDev:
      #      print ("Discovered device", dev.addr)
       # elif isNewData:
        #    print ("Received new data from", dev.addr)
def DoScan():
    # create a scanner object that sends BLE broadcast packets to the ScanDelegate
    print("inizio scansione")
    scanner = Scanner().withDelegate(ScanDelegate())
    continua_scansione=True
    #cicla con condizione
    try:
        while continua_scansione:
    # create a list of unique devices that the scanner discovered during a 10-second scan
            devices = scanner.scan(5.0)
            
                
            ggallerybeacons=[]
    # for each device  in the list of devices
            for dev in devices:
                # print  the device's MAC address, its address type,
                # and Received Signal Strength Indication that shows how strong the signal was when the script received the broadcast.
                
                #print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

                # For each of the device's advertising data items, print a description of the data type and value of the data itself
                # getScanData returns a list of tupples: adtype, desc, value
                # where AD Type means “advertising data type,” as defined by Bluetooth convention:
                # https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile
                # desc is a human-readable description of the data type and value is the data itself
                for (adtype, desc, value) in dev.getScanData():
                    #if desc=="Complete Local Name" and value=="AntoBLE":
                    #print ("RSSI=%d DB %s = %s" % (dev.rssi, desc, dev.getValueText(255)))
                    uuid = value[8:40]
                    
                    if uuid[-4:]=="1982":
                        
                        dev.major=str(int("0x"+str(value[40:44]),16))#queste due attribuzioni devono stare sotto altrimenti per ble nn beacon vanno in errore
                        dev.minor=str(int("0x"+str(value[44:48]),16))
                        ggallerybeacons.append(dev)
                        print ("rssi: "+str(dev.rssi)+" maj= "+dev.major)
                        print("trovati: "+str(len(ggallerybeacons)))
                        
                    #else:
                        #print ("no valid device found...")
                        #label2.show()
                                    
            found=next((ggallerybeacon for ggallerybeacon in ggallerybeacons if ggallerybeacon.rssi==max(ggallerybeacon.rssi for ggallerybeacon in ggallerybeacons)))
            print("fine scansione")
            label.set_text("Major: "+found.major)
            label.show()
            return 1
    except KeyboardInterrupt:
        exit()
    
label=Gtk.Label()
window = Gtk.Window()
window.maximize()
window.connect("destroy",Gtk.main_quit)

label.hide()
window.add(label)
window.show()
GLib.timeout_add(500,DoScan)#qui gira l'interfaccia grafica e cicla 
Gtk.main()
