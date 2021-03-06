import pigo
import time  # import just in case students need
import random
import datetime

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
        self.start_time = datetime.datetime.utcnow()
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 89
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 13
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
        if __name__ == "__main__":  # this makes sure the parent handler doesn't take over student's
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
                "o": ("Obstacle count", self.obstacle_count),
                "co": ("Circle count", self.circle_counting),
                "s": ("Check status", self.status),
                "t": ("Test restore heading", self.test_restore_heading),
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

    def circle_counting(self):
        count = 0
        for x in range(4):
            count += self.obstacle_count()
            self.encR(7)
        print("\n----There are totally %d objects----\n" % count)

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.stop()
        self.wide_scan(3)
        found_something = False
        counter = 0
        for distance in self.scan:
            if distance and distance < 50 and not found_something:
                found_something = True
                counter += 1
                print("Object #%d found, I think" % counter)
            if distance and distance > 50 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECT----\n" % counter)
        return counter

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

    def scan_forward(self, count=2):
        """moves servo 90 degrees and fills scan array, default count=2"""
        self.flush_scan()
        for x in range(self.MIDPOINT - 45, self.MIDPOINT + 45, count):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
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

    def restore_head(self):
        """
        Uses self.turn_track to reorient to original heading
        """
        self.stop()
        print("Restoring heading!")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))
        time.sleep(1)

    def test_restore_heading(self):
        self.encR(5)
        time.sleep(.5)
        self.encL(15)
        time.sleep(2)
        self.encR(20)
        time.sleep(2)
        self.encR(5)
        self.restore_head()

    def smart_turn(self):
        """Then in order to serve nav method, it will print the ang with greatest distance"""
        ang = 0
        largest_dist = 0
        self.wide_scan(3)
        for index, distance in enumerate(self.scan):
            if distance > largest_dist:
                largest_dist = distance
                ang = index
            elif distance == largest_dist:
                if abs(index - 90) < abs(ang - 90):
                    largest_dist = distance
                    ang = index
        print("I think the best angle is %d\n" % ang)
        turn = int(7.2 * abs(ang - self.MIDPOINT) / 90)   ##calculate how much it should turn to the valid direction.
        if ang <= self.MIDPOINT:
            print("Turn right for %d\n" % turn)
            self. encR(turn)
        time.sleep(1)
        if ang > self.MIDPOINT:
            print("Turn left for %d\n" % turn)
            self.encL(turn)
        time.sleep(1)

### Robot find a best way to move forward to reach the goal without meeting obstacles.
    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        ###formula: turning value = 7(angle with greatest distance - midpoint)/ 90
        while True:
            self.smart_turn()
            if self.dist > self.SAFE_STOP_DIST:  ###Robot will go fwd until the
                #  distance is unsafe. If it is not safe, it will do else below
                print("Ready to go!")
                self.head_fwd()
                self.cruise()
            else:
                print("Here is not safe enough, and turn back")
                self.encB(25)    # turn back
                self.restore_head()  # turn to the original direction
                time.sleep(.5)

    def smooth_turn(self):
        self.right_rot()
        start = datetime.datetime.utconw()
        while True:
            if self.dist() > 100:
                self.stop()
            elif datetime.datetime.utcnow() - start > datetime.timedetlta(seconds):
                    self.stop()
                    time.sleep(.2)

    def cruise(self):   # drive straight while path is clear or it will continue the method
        while self.dist() > self.SAFE_STOP_DIST:
                self.fwd()
                time.sleep(.1)
        else:
            print("Here is not safe enough, and turn back")

            self.encB(17)  # turn back
            self.restore_head()  # turn to the original direction
            time.sleep(.5)
            return False





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
