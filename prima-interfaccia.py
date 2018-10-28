from tkinter import *
import requests

def cerca_clicked():
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
        
 
window = Tk()
window.geometry('350x200') 
window.title("prima Antonio")
lbl = Label(window, text="Registra Utenti", font=("Arial Bold", 12))
lbl.grid(column=1,row=1)
txt= Entry(window,width=20)
txt.grid(column=1,row=2)
btn=Button(window,text="CERCA",font=("Arial Bold", 12),command=cerca_clicked)
btn.grid(column=1,row=3)
comm = Label(window, text="comunicazioni", font=("Arial Bold", 12))
comm.grid(column=1,row=10)
window.mainloop()


