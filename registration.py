from tkinter import *
import requests
import MFRC522
continue_reading = True
MIFAREReader = MFRC522.MFRC522()
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    
def cerca_clicked():
    global userid
    if len(txt.get())==0:
        comm.configure(text="nessun parametro inserito")
    else:
        print ("cerca")
        nome=txt.get()
        r = requests.get("http://www.heritagexperience.com/mw/index.php?option=com_marketwall&task=marketwalltask.getuseridfromname&username="+nome)
        userid=r.json()
        if(userid!=0):
            comm.configure(text="utente trovato, procedi con la registrazione")
                      
        else:
            comm.configure(text="utente non trovato")

def registrazione():
    
    fatto=0
    while fatto==0:
        uuid=getUuid()
        #uuid=12
        r1=requests.get("http://www.heritagexperience.com/mw/index.php?option=com_marketwall&task=marketwalltask.doregistration&userid="+str(userid)+"&uuid="+str(uuid))
        fatto=r1.json()

    comm.configure(text="registrazione avvenuta con successo")

def getUuid():
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
            return i
    

 
window = Tk()
window.geometry('700x400') 
window.title("prima Antonio")
lbl = Label(window, text="Registra Utenti", font=("Arial Bold", 6), anchor=CENTER)
lbl.grid(column=1,row=1, columnspan=2)
txt= Entry(window,width=20)
txt.grid(column=1,row=2,columnspan=2)
btn=Button(window,text="CERCA",font=("Arial Bold", 6),command=cerca_clicked)
btn.grid(column=1,row=3)
regbtn=Button(window,text="REGISTRO",font=("Arial Bold", 6),command=registrazione)
regbtn.grid(column=2,row=3)
comm = Label(window, text="", font=("Arial Bold", 6))
comm.grid(column=1,row=10)
window.mainloop()


