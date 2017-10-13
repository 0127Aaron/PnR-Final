import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 89
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 40
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 150
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 150
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        # WRITE YOUR FIRST PROJECT HERE
        if self.safety_check():
            self.head_dancing()
            self.to_the_right()
            self.head_dancing()
            self.to_the_left()
            self.head_dancing()
            self.head_fwd()
            self.now_kick()
            self.to_the_right()
            self.to_the_right()
            self.to_the_left()
            self.to_the_left()
            self.head_fwd()
            self.now_kick()
            self.head_dancing()
            self.cha_cha()
            self.stop()

        #  self.walk_it_by_yourself()
    def safety_check(self):
        self.servo(self.MIDPOINT)  # look straight ahead
        for x in range(4):     # rotate the sensor in 4 different angles
            if not self.is_clear():
                print("Not going to dance")
                self.encB(3)    # it is not safe, so go back
                self.encL(8)    # turn left
                return self.safety_check()  # do the safety check again
            self.encR(8)
            print("Check #%d" % (x + 1))
        print("Safe to dance!!")
        return True      # continue the dance method

    def head_fwd(self):     # make the sensor forward
        for x in range(1):
            self.servo(89)

    def head_dancing(self):     # the sensor turns right and turns left for 3 times
        for x in range(3):
            self.servo(49)
            self.servo(129)

    def to_the_right(self):     # the sensor turns right and the robot turns right
        for x in range(1):
            self.servo(50)
            self.encR(16)

    def to_the_left(self):      # the sensor turns left and the robot turns left
        for x in range(1):
            self.servo(130)
            self.encL(16)

    def cha_cha(self):  # robot turns right with sensor turning left,
                        # and then robot turns left with sensor turning right.
        for x in range(5):
            self.servo(109)
            self.encR(4)
            self.servo(69)
            self.encL(4)

    def now_kick(self):     # Robot goes forward for 0.5s and then goes back
        self.fwd()
        time.sleep(.5)
        self.stop()
        self.encB(5)

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        while True:
            if self.is_clear():
                print("Ready to go!")
                self.cruise()
            else:
                print("Here is not safe enough, and turn right")
                self.set_speed(100, 100)
                self.fwd()
                    time.sleep(.1)
                self.encR(8)

    def cruise(self):   # drive straight while path is clear
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.1)


####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
