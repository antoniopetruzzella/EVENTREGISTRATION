import MFRC522
import vlc
continue_reading = True
MIFAREReader = MFRC522.MFRC522()
p1 = vlc.MediaPlayer("file:////home/pi/Music/doriaDEF.mp3")
p2 = vlc.MediaPlayer("file:////home/pi/Music/ifieschiDEF.mp3")
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    

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
        if p1.is_playing()==0 and p2.is_playing()==0:
            #if i==112: 
            if i==67:  
                p1.play()
                            
            #if i==234:# and vlc.MediaPlayer.is_playing==0:
            if i==3: 
                p2.play()

            if i==2:
                p = vlc.MediaPlayer("file:////home/pi/Music/torriglia1_DEF.mp3")
        
