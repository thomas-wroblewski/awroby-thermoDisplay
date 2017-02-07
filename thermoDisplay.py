from gpiozero import LED
import signal
import sys
import os
import glob
from time import sleep
import Queue
import threading

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

tensQueue = Queue.Queue(1)
onesQueue = Queue.Queue(1)

digit1 = LED(26)
digit2 = LED(19)
aSeg = LED(22)
bSeg = LED(18)
cSeg = LED(23)
dSeg = LED(24)
eSeg = LED(25)
fSeg = LED(20)
g1Seg = LED(16)
g2Seg = LED(12)



base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def getDigits(tensQueue, onesQueue):
  while True:
    temp = read_temp()
    tens = int(temp / 10.0)
    ones = int(temp % 10.0)
    print(temp)
    tensQueue.put(tens)
    onesQueue.put(ones)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #Return F only
        return temp_f


def number( str ):
   cleanNum()
   if str == 1:
        aSeg.off()
        bSeg.on()
        cSeg.on()
        dSeg.off()
        eSeg.off()
        fSeg.off()
        g1Seg.off()
        g2Seg.off()
   elif str == 2:
        aSeg.on()
        bSeg.on()
        cSeg.off()
        dSeg.on()
        eSeg.on()
        fSeg.off()
        g1Seg.on()
        g2Seg.on()
   elif str == 3:
        aSeg.on()
        bSeg.on()
        cSeg.on()
        dSeg.on()
        eSeg.off()
        fSeg.off()     
        g1Seg.on()
        g2Seg.on()
   elif str == 4:
        aSeg.off()
        bSeg.on()
        cSeg.on()
        dSeg.off()
        eSeg.off()
        fSeg.on()
        g1Seg.on()
        g2Seg.on()
   elif str == 5:
        aSeg.on()
        bSeg.off()
        cSeg.on()
        dSeg.on()
        eSeg.off()
        fSeg.on()
        g1Seg.on()
        g2Seg.on()
   elif str == 6:
        aSeg.on()
        bSeg.off()
        cSeg.on()
        dSeg.on()
        eSeg.on()
        fSeg.on()
        g1Seg.on()
        g2Seg.on()
   elif str == 7:
        aSeg.on()
        bSeg.on()
        cSeg.on()
        dSeg.off()
        eSeg.off()
        fSeg.off()
        g1Seg.off()
        g2Seg.off()
   elif str == 8:
        aSeg.on()
        bSeg.on()
        cSeg.on()
        dSeg.on()
        eSeg.on()
        fSeg.on()
        g1Seg.on()
        g2Seg.on()
   elif str == 9:
        aSeg.on()
        bSeg.on()
        cSeg.on()
        dSeg.off()
        eSeg.off()
        fSeg.on()
        g1Seg.on()
        g2Seg.on()
   elif str == 0:
        aSeg.on()
        bSeg.on()
        cSeg.on()
        dSeg.on()
        eSeg.on()
        fSeg.on()
        g1Seg.off()
        g2Seg.off()
   else:
        cleanNum()
   return


def cleanNum( ):
        aSeg.off()
        bSeg.off()
        cSeg.off()
        dSeg.off()
        eSeg.off()
        fSeg.off()
        g1Seg.off()
        g2Seg.off()
        return

try:

    tempCheck_ = threading.Thread(target=getDigits, name="tempCheckThread-1", args=[tensQueue, onesQueue],)
    tempCheck_.setDaemon(True)
    tempCheck_.start()
    #tempCheck_.join()
    tens = 0
    ones = 0
    while True:
        #tens = int(getDigits()[0])
        #ones = int(getDigits()[1])
        if tensQueue.full():
          tens = tensQueue.get()
        if onesQueue.full():
          ones = onesQueue.get()
        digit1.off()
        number(tens)
        digit2.on()
        sleep(0.005)
        #sleep(0.1)
        digit2.off()
        number(ones)
        digit1.on()
        sleep(0.005)
        #sleep(0.1)
finally:
    cleanNum()
    print "Exiting"
