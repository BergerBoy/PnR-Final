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
    # STOP_DIST allows for robot to stop in a certain distance.
    STOP_DIST = 40
    # Experiment with different speeds to see what will get your bot to drive straight
    # RIGHT_SPEED is the speed that allows it to turn left
    # Update the number to provide more accuracy
    RIGHT_SPEED = 195
    #LEFT_SPEED is the speed that allows it to turn left
    #Update the number t provide more accuracy
    LEFT_SPEED = 200
    # This allows the robot to have more precise turns
    turn_track = 0
    # This provides a better turn method
    #The time it take for a one degree turn
    TIME_PER_DEGREE = 0.011
    # The speed the robots does to make an accurate turn
    TURN_MODIFIER = .5

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")

        # self.setSpeed
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
    def turnR(self, deg):
        #Contols the accuracy of the turn in degrees
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + "degrees away.")
        # use the setSpeed method to slow down our turns
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
        print("The exit is " + str(self.turn_track) + "degrees away!")
        # slow down for more exact turning
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #actually turn
        left_rot()
        #The time.sleep allows the robot to take a second.
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        # return speed to normal cruise speeds
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    # The setSpeed is the speed that the robot goes.
    def setSpeed(self, left, right):
        print("Left speed: " + str(left))
        print("Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)

    def backUp(self):
        if us_dist(15) < 10:
            print("Too close. Backing up for half a second")
            bwd()
            time.sleep(.5)
            self.stop()

    # AUTONOMOUS DRIVING
    # The robot has the ability to navigate.
    # Central logic loop of my navigation
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            # if it's clear in front of me...
            if self.isClear():
                # drive until something's in front of me. Good idea? you decide.
                self.cruise()
            # YOU DECIDE: check to see if you should backup?
            self.backUp()
            # IF I HAD TO STOP, PICK A BETTER PATH
            turn_target = self.kenny()
            # a positive turn is right
            if turn_target > 0:
                self.turnR(turn_target)
            # negative degrees mean left
            else:
                # let's remove the negative with abs()
                self.turnL(abs(turn_target))

    #replace turn method. Find better option
    #def kenny decides how big a turn to make to keep going
    def kenny(self):
        # Activate our scanner!
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        # YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        # YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ###########################
        ######### BUILD THE OPTIONS
        # loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                # YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    # set the counter up again for next time
                    count = 0
                    # add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        # The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        # the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption

    # SEARCH 120 DEGREES COUNTING BY 1's
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
        print("Is is clear in front of me")
        # The robot checks if the path is clear
        if self.isClear():
            #start driving forward
            fwd()
            # If the distance of the robot is less then the stop distance.
            while True:
                # break the loop if the sensor reading is closer than our stop dist
                if us_dist(15) < self.STOP_DIST:
                    break
                # You can decide how many seconds between each check
                time.sleep(.1)
        # stop if the sensor loop broke
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
