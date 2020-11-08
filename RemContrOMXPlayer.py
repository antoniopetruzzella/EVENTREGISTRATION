import urllib.request
import json
import vlc
import sys
import os
import subprocess
from subprocess import Popen
import time
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib
from gi.repository import GObject

p1 = ("/home/pi/Videos/v1.mp4")
#p2 = vlc.MediaPlayer("file:////home/pi/Music/ifieschiDEF.mp3")
p2 = ("/home/pi/Videos/v2.mp4")
omxc=None
RemoteDeviceId=1
urlGetSerial = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getserial'
urlGetStatus = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getstatus&RemoteDeviceId='+str(RemoteDeviceId)

def getResponse(url):
    with urllib.request.urlopen(url) as response:
        return response.read()
    
def DoScan():
    visitModeOn=True
    try:
        print(urlGetStatus)
        label.set_text(urlGetStatus)
        label.show()
##        #while visitModeOn:
##        print(urlGetStatus)
##        res = getResponse(urlGetStatus)
##        cont = json.loads(res.decode('utf-8'))
##        counter = 0
##        for item in cont:
##            counter += 1
##            visitModeOn=int(item["ModeVisitOn"])
##            ActualContent=item["ActualContent"]
##            
##            print(ActualContent)
##            if ActualContent==4:  
##                os.system('killall omxplayer.bin')
##                continue_reading=False
##                omxc=Popen(['omxplayer','-b', p1])
##                            
##            #if i==234:# and vlc.MediaPlayer.is_playing==0:
##            if ActualContent==3: 
##                #p2.play()
##                os.system('killall omxplayer.bin')
##                continue_reading=False
##                omxc=Popen(['omxplayer','-b', p2])
##                omxc.communicate()
##                print (omxc.pid)
##                omxc.terminate()
        
    except KeyboardInterrupt:
        exit()
        
GObject.timeout_add(1000,DoScan)#qui gira l'interfaccia grafica e cicla 
GObject.threads_init()   
label=Gtk.Label()
window = Gtk.Window()
window.maximize()
window.connect("destroy",Gtk.main_quit)

label.hide()
window.add(label)
window.show()

Gtk.main()

