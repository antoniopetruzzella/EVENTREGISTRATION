from tkinter import *
import requests
import MFRC522
import threading

continue_reading = True
MIFAREReader = MFRC522.MFRC522()
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    
def cerca_utente(uuid):
    
    print (str(uuid))
    r = requests.get("http://www.heritagexperience.com/mw/index.php?option=com_marketwall&task=marketwalltask.getusernamefromuuid&uuid="+str(uuid))
    print(r.url)
    username=r.json()
    comm.configure(text=username)
    print(username)
    
    
                             
def scanning():
    continue_reading = True
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
            print(uid)
            continue_reading = False
            cerca_utente(uid[0])
            
    window.after(1000,scanning)            
  

window = Tk()
window.geometry('350x200')
window.title("prima Antonio")
comm = Label(window, text="leggo utente", font=("Arial Bold", 6))
comm.grid(column=1,row=1)
#btn=Button(window,text="CERCA",font=("Arial Bold", 6),command=scanning)
#btn.grid(column=1,row=2)
window.after(1000,scanning)
window.mainloop()
#thread=threading.Thread(target=scanning)
#thread.start()  


        
