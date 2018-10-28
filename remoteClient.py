import requests;
import smtplib;

url="http://www.heritagexperience.com/raspberryWS/raspberryloaddataWS.php?action=";

def writeDataInt(url,descrizione,value):
    url=url+"insertdata&descrizione=";
    r = requests.put(url+descrizione+"&valueInt="+str(value));
    print (r);
    return;

def readDataInt(url_,descrizione):
    print("prova di lettura da remoto...");
    url_=url_+"readdata&descrizione=";
    #print(url_+descrizione);
    r = requests.put(url_+descrizione);
    rjs=r.json();
    #print (rjs);
    
    msg="\r\n ciao! "
    for item in rjs:
        msg=msg+item['descrizione']+':'+item['valueInt']+' '
        
    print (msg)
    #msg=self.getVer();
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    #server.starttls()
    server.login("a.petruzzella71@gmail.com", "Ortigia1971")
    
    server.sendmail("a.petruzzella71@gmail.com", "a.petruzzella71@gmail.com", msg)
    return;
    

#writeDataInt("provadaFunzione",24000);
readDataInt(url,"provadaFunzione");
