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
    # STOP_DIST allows for robot to stop, check its path and make sure that nothing is in its way.
    STOP_DIST = 40
    # Experiment with different speeds to see what will get your bot to drive straight
    # RIGHT_SPEED is the speed that allows it to turn left
    # Update the number to provide more accuracy
    RIGHT_SPEED = 200
    #LEFT_SPEED is the speed that allows it to turn left
    #Update the number t provide more accuracy
    LEFT_SPEED = 200
    # explain what the item below is used for
    turn_track = 0
    # This provides a better turn method
    #The time it take for a one degree turn
    TIME_PER_DEGREE = 0.011
    # The speed the robots does to make an accurate turn
    TURN_MODIFIER = .5

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")

        # explain what the item below is used for
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
        print('it is safe to dance')
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
                x += 25
                stop()

    ###MY NEW TURN METHODS because encR and encL dont get it
    # Takes number of degrees and right according????????
    def turnR(self, deg):
        #Contols the accuracy of the turn in degrees
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + "degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)

        # actually turn
        right_rot()
        # by using the data from our turn experiment calculate how long we need to turn for
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        # return to normal speed
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    # explain what the item below is used for
    def turnL(self, deg):
        # adjust tracker to see how many degrees away the turn is
        self.turn_track -= deg
        print("The exit is " + str.(self.turn_track) + "degrees away!")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        # do stuff
        left_rot()
        # explain what the item below is used for
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    # explain what the item below is used for
    def setSpeed(self, left, right):
        print("Left speed: " + str(left))
        print("Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)

    # AUTONOMOUS DRIVING
    # Explain the purpose of the method
    # Central logic loop of my navigation
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        # TODO: If while loop fails, check for other paths
        while True:
            # TODO: Replace choosePath with a method that's smarter.
            self.cruise()
            answer = self.choosePath()
            if answer == "left":
                # TODO: Replace '45' with a variable representing a smarter option
                self.encL(5)
            elif answer == "right":
                # TODO: Replace '45' with a variable representing a smarter option
                self.encR(5)
                # lets go foward just a little bit

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wideScan(self):
        # dump all values
        self.flushScan()
        # Change the 5 and .05 for more accuracy
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +1):
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
        # AVERAGING THE RIGHT SIDE
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        # AVERAGING THE LEFT SIDE
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    # cruise method
    def cruise(self):
        servo(self.MIDPOINT)
        # TODO: Replace below with a single setSpeed method
        set_left_speed(self.LEFT_SPEED)
        set_right_speed(self.RIGHT_SPEED)
        print("Is is clear in front of me")
        # explain what the item below is used for
        if self.isClear():
            fwd()
            # explain what the item below is used for
            while True:
                if us_dist(15) < self.STOP_DIST:
                    break
                time.sleep(.1)
        self.stop()


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
Sign
up
for free
