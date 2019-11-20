import RPi.GPIO as GPIO
import time
import queue

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.IN)         # PIR to first signal
GPIO.setup(14, GPIO.IN)         # PIR to second signal
GPIO.setup(4, GPIO.IN)          # PIR to third signal
GPIO.setup(10, GPIO.IN)         # PIR to fourth signal
L = queue.Queue(maxsize=4)
green_time = 3
yellow_time = 2
tt1 = 0
tt2 = 0
tt3 = 0
tt4 = 0
firebase = firebase.FirebaseApplication('https://raspberrypi-2d135.firebaseio.com/')

def activate1():
    # First signal G->Y->R
    GPIO.output(18, GPIO.HIGH)
    time.sleep(green_time)
    GPIO.output(18, GPIO.LOW)
    time.sleep(yellow_time)
    GPIO.output(15, GPIO.HIGH)
    tt1 = tt1 + green_time + yellow_time
    result = firebase.post('https://raspberrypi-2d135.firebaseio.com/', {'tt1':str(tt1),'tt2':str(tt2), 'tt3':str(tt3), 'tt4':str(tt4)})
    
def activate2():
    # Second signal G->Y->R
    GPIO.output(24, GPIO.HIGH)
    time.sleep(green_time)
    GPIO.output(24, GPIO.LOW)
    time.sleep(yellow_time)
    GPIO.output(23, GPIO.HIGH)
    tt2 = tt2 + green_time + yellow_time    
    result = firebase.post('https://raspberrypi-2d135.firebaseio.com/', {'tt1':str(tt1),'tt2':str(tt2), 'tt3':str(tt3), 'tt4':str(tt4)})

def activate3():
    # Third signal G->Y->R
    GPIO.output(3, GPIO.HIGH)
    time.sleep(green_time)
    GPIO.output(3, GPIO.LOW)
    time.sleep(yellow_time)
    GPIO.output(2, GPIO.HIGH)
    tt3 = tt3 + green_time + yellow_time
    result = firebase.post('https://raspberrypi-2d135.firebaseio.com/', {'tt1':str(tt1),'tt2':str(tt2), 'tt3':str(tt3), 'tt4':str(tt4)})

def activate4():
    # Fourth signal G->Y->R
    GPIO.output(27, GPIO.HIGH)
    time.sleep(green_time)
    GPIO.output(27, GPIO.LOW)
    time.sleep(yellow_time)
    GPIO.output(17, GPIO.HIGH)
    tt4 = tt4 + green_time + yellow_time
    result = firebase.post('https://raspberrypi-2d135.firebaseio.com/', {'tt1':str(tt1),'tt2':str(tt2), 'tt3':str(tt3), 'tt4':str(tt4)})
    
def clear_queue():
    while(!L.empty()):
        current = L.get()
        if(current == 1):
            activate1()
        elif(current == 2):
            activate2()
        elif(current == 3):
            activate3()
        elif(current == 4):
            activate4()
        
def fill_queue():                                           # No duplicate checking
    if(GPIO.input(22) == True and !L.full()):
        L.put(1)
    if(GPIO.input(14) == True and !L.full()):
        L.put(2)
    if(GPIO.input(4) == True and !L.full()):
        L.put(3)
    if(GPIO.input(10) == True and !L.full()):
        L.put(4)

def analyse():
        busiest = max(tt1, tt2, tt3, tt4)
        least_busy = min(tt1, tt2, tt3, tt4)
        if(busiest == least_busy):
            print("All roads are equally busy")
        else: 
            if(tt1 == busiest):
                print("The busiest road as of now is Road 1")
            elif(tt2 == busiest):
                print("The busiest road as of now is Road 2")
            elif(tt3 == busiest):
                print("The busiest road as of now is Road 3")
            elif(tt4 == busiest):
                print("The busiest road as of now is Road 4")

            if(tt1 == least_busy):
                print("This traffic can be diverted to Road 1, having the least traffic")
            elif(tt2 == least_busy):
                print("This traffic can be diverted to Road 2, having the least traffic")
            elif(tt3 == least_busy):
                print("This traffic can be diverted to Road 3, having the least traffic")
            elif(tt4 == least_busy):
                print("This traffic can be diverted to Road 4, having the least traffic")

i = 0;
while(True):

    clear_queue()
    fill_queue()
    activate1()
    
    clear_queue()
    fill_queue()
    activate2()
    
    clear_queue()
    fill_queue()
    activate3()
    
    clear_queue()
    fill_queue()
    activate4()
    
    # if pir motion sensor detects motion
    analyse()

GPIO.cleanup()
    
# Install the Firebase package using the command

# $  sudo pip install python-firebase

# // Initialize queue
# Syntax: queue.Queue(maxsize)

# // Insert Element
# Syntax: Queue.put(data)

# // Get And remove the element
# Syntax: Queue.get()

# Return Boolean for Full 
# Queue 
# print("Full: ", L.full())

# Return Boolean for Empty 
# Queue 
# print("Empty: ", L.empty()) 
