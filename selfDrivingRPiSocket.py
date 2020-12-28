import socket
import RPi.GPIO as GPIO

def stop(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.LOW)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.LOW)
    

c = socket.socket()
compIP = input("enter the ip of the computer")
c.connect((compIP,9999))

def front(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.HIGH)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.HIGH)

def softRightFront(left1,left2,right1,right2):
    GPIO.output(left1,GPIO.LOW)
    GPIO.output(left2,GPIO.HIGH)
    GPIO.output(right1,GPIO.LOW)
    GPIO.output(right2,GPIO.LOW)

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

try:
    while True:
        instruction = c.recv(1024).decode()
        print(instruction)
        if instruction == "front":
            front(left1,left2,right1,right2)
            print("front")
        elif instruction =="softRightFront":
            softRightFront(left1,left2,right1,right2)
            print("softRightFront")
        elif instruction == "close socket":
            print("stopping")
            stop(left1,left2,right1,right2)
            GPIO.cleanup()
            break
except KeyboardInterrupt:
        print("stopping")
        stop(left1,left2,right1,right2)
        GPIO.cleanup()