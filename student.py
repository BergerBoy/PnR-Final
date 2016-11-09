import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 106
    STOP_DIST = 20
    RIGHT_SPEED = 200
    LEFT_SPEED = 200

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        # self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        print ('it is safe to dance')
        for x in range(100, 200, 25):
            while self.isClear() and x <= 200:
                self.encR(18)
                print('Speed is set to' + str(x))
                set_speed(x)
                servo(20)
                self.encB(20)
                self.encR(16)
                self.encL(20)
                self.encF(16)
                servo(120)
                time.sleep(.1)
                x +=25
                stop()


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for other paths
        while True:
            while self.isClear():
                self.encF(10)
            answer = self.choosePath()
            if answer == "left":
                self.encL(5)
            elif answer == "right":
                self.encR(5)
            #lets go foward just a little bit

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wideScan(self):
        # dump all values
        self.flushScan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +5):
            servo(x)
            time.sleep(.05)
            scan1 = us_dist(15)
            time.sleep(.05)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)

    # DECIDE WHICH WAY TO TURN
    def choosePath(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.wideScan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    #cruise method
    def cruise(self):
        set_left_speed (190)
        set_right_speed (190)
        print("Is is clear in front of me")
        clear = self.isClear()
        print(clear)
        while True:
            if clear:
                print("Go Go Go!!!")
                fwd()
            if not self.isClear():
                print("STOP")
                self.stop()
                if answer == "left":
                    self.encL(5)
                elif answer == "right":
                    self.encR(5)


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
