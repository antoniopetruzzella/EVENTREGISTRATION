import os.path
import sys
import gi
import urllib.request
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import vlc
from gi.repository import GObject

MRL="";
RemoteDeviceId=1
urlGetSerial = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getserial'
urlGetStatus = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getstatus&RemoteDeviceID='+str(RemoteDeviceId)



class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused=False
        self.is_player_active = False
        self.connect("destroy",Gtk.main_quit)
           
    def show(self):
        self.show_all()
        
    def setup_objects_and_events(self):
       
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300,300)
        self.draw_area.connect("realize",self._realized)
        self.name_label=Gtk.Label()
        self.name_label.set_text("in attesa di connessione")
        self.name_label.set_property("height-request", 30)
        self.hbox = Gtk.Box(spacing=6)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        self.hbox.pack_start(self.name_label,True, True,0)
        
    def runDoCycle(self):
        GObject.timeout_add(3000,self.doCycle)
        
   
        
    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        #self.player.set_mrl(MRL)
        #self.player.play()
        
        #self.is_player_active = True
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.EventManager)
        
    def EventManager(self, event):
        if event.type == vlc.EventType.MediaPlayerEndReached:
            print ("Event reports - finished, playing next")
            self.is_player_active=False
            
    def doCycle(self):

        visitModeOn=True
        #print('ciao')
        
        try:
            
            #while visitModeOn:
            if self.is_player_active==False : #PRIMA DI TUTTO NON DEVE ESSERCI VIDEO ON
                print(urlGetStatus)
                res = self.getResponse(urlGetStatus)
                cont = json.loads(res.decode('utf-8'))
                counter = 0
                for item in cont:
                    counter += 1
                    sessionUser=item["SessionUser"]
                    sessionCode=item["SessionCode"]
                    sessionModeStatus=int(item["SessionModeStatus"])
                    actualContent=item["ActualContent"]
                    #print(ActualContent)
                    if sessionModeStatus==1: #la sessione è aperta
                        if sessionUser!=None: # la sessione è proprietà
                            self.name_label.set_text(sessionUser)
                            if actualContent!=None:
                                MRL = "/home/pi/Videos/0"+actualContent+"_.mp4"
                            else:
                                MRL = "/home/pi/Pictures/panorama-toscana.jpg"
                            print(str(self.is_player_active))
                            if os.path.isfile(MRL):
                                self.is_player_active=True
                            else:
                                #print("file mancante")
                                MRL = "/home/pi/Pictures/panorama-toscana.jpg"
                                self.is_player_active=False
                            self.player.set_mrl(MRL)
                            self.player.play()
                        else: #non c'è sessionUser
                            print ("manca il sessionUser")
                            #allora devo mettere a monitor il prossimo codice
                            #libero
                            self.name_label.set_text("devi inserire il codice: "+sessionCode)
                            MRL = "/home/pi/Pictures/panorama-toscana.jpg"
                            self.player.set_mrl(MRL)
                            self.player.play()
                            
                    else: #la Sessione è finita
                        print ("sessione finita")
                        
                        #allora devo produrre una nuova riga di sessione
                        #con codice e utente null
                        
            return True
        except KeyboardInterrupt:
            exit()

    
    def getResponse(self,url):
        with urllib.request.urlopen(url) as response:
            return response.read()



MRL = "/home/pi/Pictures/panorama-toscana.jpg"
Username=""
window = ApplicationWindow()
window.setup_objects_and_events()
window.show()
window.runDoCycle()
Gtk.main()
#window.player.stop()
#window.vlcInstance.release()
