import MFRC522
import vlc
import sys
import os
from subprocess import Popen
p2 = ("/home/pi/Videos/v2.mp4")
#os.system('killall omxplayer.bin')
omxc=Popen(['omxplayer', p2])
print (omxc)
