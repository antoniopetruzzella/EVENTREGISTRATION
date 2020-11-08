# test BLE Scanning software
# jcs 6/8/2014

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

# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

# create a list of unique devices that the scanner discovered during a 10-second scan
devices = scanner.scan(10.0)

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
            print("UUID: "+uuid)
            print ("MAJOR: "+str(int("0x"+str(value[40:44]),16)))
            print ("MINOR: "+str(int("0x"+str(value[44:48]),16)))

            #print("0x"+str(value[40:44]))	
        #per=Peripheral(dev.addr)
        #c=per.getCharacteristics(1,0xFFFF,"beb5483e-36e1-4688-b7f5-ea07361b26a8")
            #for cc in c:
                #print ("%s" % cc.read().decode())
                #per.disconnect()    
                                

                
