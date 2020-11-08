import MFRC522
import vlc
import sys
import os
import subprocess
from subprocess import Popen
continue_reading = True
MIFAREReader = MFRC522.MFRC522()
#p1 = vlc.MediaPlayer("file:////home/pi/Music/doriaDEF.mp3")
p1 = ("/home/pi/Videos/v1.mp4")
#p2 = vlc.MediaPlayer("file:////home/pi/Music/ifieschiDEF.mp3")
p2 = ("/home/pi/Videos/v2.mp4")
# Capture SIGINT for cleanup when the script is aborted

omxc=None
   
try:
    while continue_reading:
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        
        # If a card is found
        #if status == MIFAREReader.MI_OK:
            #print ("Card detected")
            
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
           
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
                
            print ("UID:"+str(uid[0]))
            i=uid[0]
            
            #if omxc.poll()==None:
                #if i==112: 
            if i==67:  
                os.system('killall omxplayer.bin')
                continue_reading=False
                omxc=Popen(['omxplayer','-b', p1])
                                
                #if i==234:# and vlc.MediaPlayer.is_playing==0:
            if i==3: 
                    #p2.play()
                os.system('killall omxplayer.bin')
                continue_reading=False
                omxc=Popen(['omxplayer','-b', p2])
                omxc.communicate()
                print (omxc.pid)
                omxc.terminate()

except KeyboardInterrupt:
    
    omxc.terminate()
                    
            
