import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
print (GPIO.RPI_REVISION)
i=1
while (i<28):
    GPIO.setup(i,GPIO.OUT)
    print ("lettura GPIO"+str(i))
    print ("valore: "+str(GPIO.input(i)))
    i+=1
GPIO.cleanup()    
print ("fine esecuzione")
