# the basic strucure of this settings file is inspired by a
# youtube tutorial by "KidsCanCode" released in january 2016:
# https://youtu.be/uWvb3QzA48c

# video settings
WIDTH = int(1920/4*3)
HEIGHT = int(1080/4*3)
FPS = 60
TITLE = "corona universalis (working title)"
TILESIZE = 12
SHOW_FPS = True
SHOW_INFECTED = True

# game settings
CAMERA_SPEED = 15*60/FPS
TIMEOFMONTH = 20*FPS  # number of seconds it takes to advance one month
STARTMONEY = 70
MONEYEARNING = 10  # how much money you get per week (default value)
# building settings
TESTCENTER_RANGE = 200
TESTCENTER_PRICE = 10
TESTCENTER_TIME = 5
HOSPITAL_RANGE = 150
HOSPITAL_PRICE = 100
HOSPITAL_TIME = 20
VACCINECENTER_RANGE = 100
VACCINECENTER_PRICE = 400
VACCINECENTER_TIME = 30

# colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY50 = (50, 50, 50)
GREY150 = (150, 150, 150)
GREY222 = (222, 222, 222)
RED = (255, 0, 0)
MAGENTA = (139, 0, 139)
DARKPURPLE = (96, 43, 112)

# lists
HUMANS_LIST = []

# Human settings
HUMAN_SIZE = 10  # how tall the Humans are (in pixels)
WALKCYCLE = 100  # how often the humans move in random directions
WALKDISTANCE = 7  # how many frames they should walk in a random direction
INITIAL_INFECTION_CHANCE = 1  # percentage of humans that spawn infected (standard value = 1)
INFECT_CHANCE = 5   # number of seconds of contact it takes for (on average) of infection after one second contact
ILL_CHANCE = 200  # number of seconds of being infected it takes for humans to become ill
HUMAN_COUNT = 2500

# fonts
SMALLFONT = "assets/munro-small.ttf"
BIGFONT = "assets/munro-small.ttf"
