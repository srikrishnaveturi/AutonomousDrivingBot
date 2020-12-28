from socket import *
import RPi.GPIO as GPIO
import time
import os
import cv2

pictureNumDict = {'front' : 0,
                  'softRightFront' : 0,
                  'right' : 0,
                  'softRightBack' : 0,
                  'back' : 0,
                  'softLeftBack' : 0,
                  'left' : 0,
                  'softLeftFront' : 0}

print("Giving some time to the camera to initialize")
cap = cv2.VideoCapture(0)
#setting smaller image sizes for faster processing
cap.set(3, 448)
cap.set(4, 448)
time.sleep(1.5)
print("camera ready,hopefully")
def takePicture(direction):
    global pictureNumDict,cap
    try:
        os.chdir(f'/home/pi/Desktop/Self driving/images/{direction}')
    except:
        os.mkdir(f'/home/pi/Desktop/Self driving/images/{direction}')
        os.chdir(f'/home/pi/Desktop/Self driving/images/{direction}')
    pictureNumDict[direction] += 1
    _,frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame = cv2.resize(frame, (224,224), interpolation =cv2.INTER_AREA)
    cv2.imwrite(f'{pictureNumDict[direction]}.jpeg',frame)
    
def front(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.HIGH)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.HIGH)
    takePicture("front")

def back(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.HIGH)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.HIGH)
    GPIO.output(right2,GPIO.LOW)
    takePicture("back")

    
def left(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.HIGH)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.HIGH)
    takePicture("left")
                    
    
def softLeftFront(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.HIGH)
    takePicture("softLeftFront")
    
def softLeftBack(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.HIGH)
    GPIO.output(right2,GPIO.LOW)
    takePicture("softLeftBack")
    

def right(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.HIGH)
    GPIO.output(right1,GPIO.HIGH)
    GPIO.output(right2,GPIO.LOW)
    takePicture("right")

def softRightFront(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.HIGH)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.LOW)
    takePicture("softRightFront")
    
def softRightBack(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.HIGH)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.LOW)
    takePicture("softRightBack")
    
    
def stop(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.LOW)
    
def main():
    global cap
    
    left1 = 6
    left2 = 13
    right1 = 19
    right2 = 26
    enableLeft = 14
    enableRight = 15
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left1,GPIO.OUT)
    GPIO.setup(left2,GPIO.OUT)
    GPIO.setup(right1,GPIO.OUT)
    GPIO.setup(right2,GPIO.OUT)
    GPIO.setup(enableLeft,GPIO.OUT)
    GPIO.setup(enableRight,GPIO.OUT)
    p1=GPIO.PWM(enableLeft,1000)
    p1.start(90)
    p2=GPIO.PWM(enableRight,1000)
    p2.start(90)
    
    stop(left1,left2,right1,right2)
    s = socket(AF_INET, SOCK_DGRAM)
    print("socket created")
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ip = input("enter IP address of the RPi : ")
    s.bind((ip,9999))
    print("Enter ^C to stop")
    try:
        while True:
            print("Waiting for data...")
            data, addr = s.recvfrom(1024) # blocking
            instruction = data.decode("utf-8")
            #print(instruction)
            instruction = instruction.split()
            if len(instruction) == 3:
                power = instruction[0]
                angle = float(instruction[1])
                speed = float(instruction[2])
                print("power",power)
                print("angle",angle)
                print("speed",speed)
                if power == "off":
                    print("power is off")
                    stop(left1,left2,right1,right2)
                elif speed > 0.7:
                    if angle > 337.5 or angle < 22.5:
                        print("front")
                        front(left1,left2,right1,right2)
                    elif angle > 22.5 and angle < 67.5:
                        print("soft right front")
                        softRightFront(left1,left2,right1,right2)
                        
                    elif angle > 67.5 and angle < 112.5:
                        print("right turn")
                        #1right(left1,left2,right1,right2)
                        
                    elif angle > 112.5 and angle < 157.5:
                        print("soft right back")
                        softRightBack(left1,left2,right1,right2)
                    
                    elif angle > 157.5 and angle < 202.5:
                        print("back")
                        back(left1,left2,right1,right2)
                    
                    elif angle > 202.5 and angle < 247.5:
                        print("soft left back")
                        softLeftBack(left1,left2,right1,right2)
                    
                    elif angle > 247.5 and angle < 292.5:
                        print("left")
                        left(left1,left2,right1,right2)
                    
                    elif angle > 292.5 and angle < 337.5:
                        print("soft left front")
                        softLeftFront(left1,left2,right1,right2)    
                else:
                    print("stop")
                    stop(left1,left2,right1,right2)   
            else:
                print("please press on/off button once on the app!")
            
    except KeyboardInterrupt:
        print("stopping")
        cap.release()
        cv2.destroyAllWindows
        GPIO.cleanup()

main()