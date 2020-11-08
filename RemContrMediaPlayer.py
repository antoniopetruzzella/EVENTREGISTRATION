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
urlGetStatus = 'http://demo.ggallery.it/GGARBACK/index.php?option=com_ggne&task=remotecontroller.getstatus&RemoteDeviceId='+str(RemoteDeviceId)



class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused=False
        self.is_player_active = False
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
        
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300,300)
        
        self.draw_area.connect("realize",self._realized)
        
        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        
    def runDoCycle(self):
        GObject.timeout_add(3000,self.doCycle)
        
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
        self.is_player_active = True
        
    def doCycle(self):

        visitModeOn=True
        #print('ciao')
        
        try:
            
            #while visitModeOn:
            print(urlGetStatus)
            res = self.getResponse(urlGetStatus)
            cont = json.loads(res.decode('utf-8'))
            counter = 0
            for item in cont:
                counter += 1
                visitModeOn=int(item["ModeVisitOn"])
                ActualContent=item["ActualContent"]
                MRL = "/home/pi/Videos/0"+ActualContent+".mp4"
                
                #if window.is_player_active==False :
                print(MRL)
                window.player.set_mrl(MRL)
                window.player.play()
            return True
        except KeyboardInterrupt:
            exit()

    def getResponse(self,url):
        with urllib.request.urlopen(url) as response:
            return response.read()



        
#MRL = "/home/pi/Videos/04.mp4"
window = ApplicationWindow()
window.setup_objects_and_events()
window.show()
window.runDoCycle()
Gtk.main()
#window.player.stop()
#window.vlcInstance.release()
