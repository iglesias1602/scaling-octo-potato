from io import *
from machine import Pin
import utime
import math

pin_trigger = Pin(3, Pin.OUT)
pin_echo = Pin(4, Pin.IN)

led_red = Pin(0, Pin.OUT)
led_green = Pin(1, Pin.OUT)


valeur = 1

# Left Display
Ag = Pin(6,Pin.OUT) # Top
Bg = Pin(7,Pin.OUT) # Top Right
Cg = Pin(8,Pin.OUT) # Bottom Right
Dg = Pin(9,Pin.OUT) # Bottom
Eg = Pin(10,Pin.OUT)# Bottom Left
Fg = Pin(11,Pin.OUT)# Top Left
Gg = Pin(13, Pin.OUT)# Middle
DPg = Pin(12,Pin.OUT) # Decimal Point

# Right Display
Ad = Pin(22,Pin.OUT)    # Top
Bd = Pin(21,Pin.OUT)    # Top Right
Cd = Pin(20,Pin.OUT)    # Bottom Right
Dd = Pin(19,Pin.OUT)    # Bottom
Ed = Pin(18,Pin.OUT)    # Bottom Left
Fd = Pin(17,Pin.OUT)    # Top Left
Gd = Pin(16, Pin.OUT)   # Middle


leftDisplay = [Ag, Bg, Cg, Dg, Eg, Fg, Gg, DPg] # Left Display
rightDisplay = [Ad, Bd, Cd, Dd, Ed, Fd, Gd]    # Right Display

#common anode 7 segment
chars = [
    [0,0,0,0,0,0,1,1], #0
    [1,0,0,1,1,1,1,1], #1
    [0,0,1,0,0,1,0,1], #2
    [0,0,0,0,1,1,0,1], #3
    [1,0,0,1,1,0,0,1], #4
    [0,1,0,0,1,0,0,1], #5
    [0,1,0,0,0,0,0,1], #6
    [0,0,0,1,1,1,1,1], #7
    [0,0,0,0,0,0,0,1], #8
    [0,0,0,0,1,0,0,1], #9
    ]


def count(display, number):
    if display == leftDisplay:
        for i in range(len(leftDisplay)):
            leftDisplay[i].value(chars[number][i])
    if display == rightDisplay:
        for j in range(len(rightDisplay)):
            rightDisplay[j].value(chars[number][j])
    
def clear():
    for i in leftDisplay:
        i.value(1)
    for j in rightDisplay:
        j.value(1)

def check(timer1):
    global valeur
    if valeur < 10:
        count(rightDisplay, valeur)
    elif valeur >= 10 and valeur < 100:
        count(leftDisplay, valeur//10)
        count(rightDisplay, valeur%10)
    elif valeur >= 100:
        count(leftDisplay, valeur//100)
        DPg.value(0)
        count(rightDisplay, (valeur%100)//10)


def init_timer():
    timer1 = Timer()
    timer1.init(freq=100.0,mode=Timer.PERIODIC,callback=check)

def init():
    init_timer()

def main_loop():
    global valeur
    # Pull the trigger low and pause
    pin_trigger.low()
    utime.sleep_us(2)
    
    # Pull the trigger high for 5 us
    pin_trigger.high()
    utime.sleep_us(5)
    
    # Pull the trigger low
    pin_trigger.low()
    
    # Wait when echo is low and add timestamp for it
    while pin_echo.value() == 0:
        signal_off = utime.ticks_us()
    
    # Wait when echo is high and add timestamp for it
    while pin_echo.value() == 1:
        signal_on = utime.ticks_us()
        
    # Calculate time between on and of signal
    timepassed = signal_on - signal_off
    
    # Multiply the journey time by the speed of souind 0.0343 cm per microsecond
    object_distance = math.floor((timepassed * 0.0343) / 2)
    
    print("The distance from object is ",object_distance,"cm")
    valeur = object_distance

    if object_distance == 24:
        led_red.value(0)
        led_green.value(1)
    else:
        led_red.value(1)
        led_green.value(0)
    print(valeur)
    utime.sleep_ms(500)
    

init()
while 1:
    main_loop()
    print(valeur)
    #utime.sleep_ms(20)
    clear()

