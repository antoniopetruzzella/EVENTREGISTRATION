import os.path
import sys
import gi
import urllib.request
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib,Gdk
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import vlc
from gi.repository import GObject
from bluepy.bluepy.btle import Scanner, DefaultDelegate, Peripheral,UUID
MRL="";
RemoteDeviceId=1
urlGetSerial = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getserial'
urlGetStatus = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getstatus&RemoteDeviceId='+str(RemoteDeviceId)



class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="POSTAZIONE UNO")
        self.player_paused=False
        self.is_player_active = False
        self.is_fullscreen=False
        self.connect("destroy",Gtk.main_quit)
           
    def show(self):
        self.show_all()
        
    def setup_objects_and_events(self):
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()
        
        self.play_image = Gtk.Image.new_from_icon_name(
                "gtk-media-play",
                Gtk.IconSize.MENU
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "gtk-media-pause",
                Gtk.IconSize.MENU
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "gtk-media-stop",
                Gtk.IconSize.MENU
            )
        
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)

        self.name_label=Gtk.Label()
        self.name_label.set_text("in attesa di connessione")
        
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(250,250)
        
        self.draw_area.connect("realize",self._realized)
        
        self.hbox = Gtk.Box(spacing=6)
##        self.hbox.pack_start(self.playback_button, True, True, 0)
##        self.hbox.pack_start(self.stop_button, True, True, 0)
        self.hbox.pack_start(self.name_label,True, True,0)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        
    def runDoCycle(self):
##        self.player.set_mrl(MRL)
##        self.player.play()
        print ("cerco di connettermi")
        per=Peripheral("d7:84:e7:e2:87:68")
        #per.setDelegate( MyDelegate() )
        print("connessione avvenuta")
        GObject.timeout_add(3000,self.doCycle,per)
        
    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)
        
    def toggle_player_playback(self, widget, data=None):

        """
        Handler for Player's Playback Button (Play/Pause).
        """

        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass
        
    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.EventManager)
        
    def EventManager(self, event):
        if event.type == vlc.EventType.MediaPlayerEndReached:
            print ("Event reports - finished, playing next")
            self.is_player_active=False
        if event.type == vlc.EventType.MediaPlayerEncounteredError:
            print ("Event reports - some error")
            self.is_player_active=False
            
    def doCycle(self,per):

        visitModeOn=True
        #print('ciao')
        
        try:
            
            #while visitModeOn:
            #print("stato player:",str(self.is_player_active))
            if self.is_player_active==False :
                c=per.getServices()
                
                for cc in c:
                    try:
                        #print ("serv. uuid"+cc.uuid.getCommonName())
                        if cc.uuid.getCommonName()=="19b10000-e8f2-537e-4f6c-d104768a1214":
                            #print("trovato il servizio")    
                            ccc=cc.getCharacteristics()
                            for cccc in ccc:
                                #print("char. uuid: "+ cccc.uuid.getCommonName())
                                #print("char. value"+str(cccc.read()))
                                #print("char. value: "+str(int.from_bytes(cccc.read(),byteorder='little', signed=True)))
                                try:    
                                    value=cccc.read()
                                    if cccc.uuid.getCommonName()=="19b10001-e8f2-537e-4f6c-d104768a1215":
                                        
                                        
                                        #print("secondo char:", value.decode('utf-8'))
                                        Username=value.decode('utf-8')
                                        self.name_label.set_text("utente connesso: "+Username)
                                    if cccc.uuid.getCommonName()=="19b10001-e8f2-537e-4f6c-d104768a1214":
                                        
                                        
                                        ActualContent=int.from_bytes(value,byteorder='little', signed=True)
                                        MRL = "/home/pi/Videos/0"+str(ActualContent)+".mp4"
                                        #print("stato player:",str(self.is_player_active))
                                        #print(MRL)
                                        
                                        if os.path.isfile(MRL):
                                            self.player.set_mrl(MRL)
                                            self.player.play()
                                            self.is_player_active=True
                                        else:
                                            #print("file mancante")
                                            self.is_player_active=False
                                        
                                            
                                except:
                                    #print("error in read charact. value:", sys.exc_info()[0])
                                    self.is_player_active=False
                                    pass
                    except:
                        print("error in doCycle:", sys.exc_info()[0])
                        self.is_player_active=False
                        continue
                             
                            
                    #per.disconnect()
            return True
        except KeyboardInterrupt:
            exit()
        except:
            print("error:", sys.exc_info()[0])
                
            return True


    def getResponse(self,url):
        with urllib.request.urlopen(url) as response:
            return response.read()

    def fullscreen_toggler(self, widget, ev):
        #
        
        if ev.keyval==65480:
            print("is_fullscreen",self.is_fullscreen)
            if self.is_fullscreen:
                window.unfullscreen()
                print("tolgo")
            else:
                window.fullscreen()
                print("metto")
                
    def on_window_state_event(self, widget, ev):
        self.is_fullscreen = bool(Gdk.WindowState.FULLSCREEN & ev.new_window_state)

MRL = "/home/pi/Pictures/panorama-toscana.jpg"
Username=""

window = ApplicationWindow()
window.setup_objects_and_events()
window.connect('key-press-event', window.fullscreen_toggler)
window.connect("window-state-event", window.on_window_state_event)
#window.fullscreen()
window.show()
window.runDoCycle()
Gtk.main()
#window.player.stop()
#window.vlcInstance.release()
