from time import sleep
from winsound import Beep #Will need to import everything for servo control
print " _____    ______     _____      _____ "
print "| / \ |  |  ____|   /  _  \    /  _  \ "
print "| | / /  | |____   |  / \  |  |  / \  | "
print "| | \ \   \____ \  |  | |  |  |  | |  | "
print "| |  | |  ____| |  |  \_/  |  |  \_/  | "
print "|_|  |_| |______/   \_____/    \_____/ "

def T2():
    T2 = Beep(500,500) #This will be the function to call the servo to move

def T4():
    T4 = Beep(800,500) #Same

T5 = "You selected T2" #Just a copy and paste from earlier.
T6 = "You selected T2"
T7 = "You selected T2"
T8 = "You selected T2"
T9 = "You selected T2"
T11 = "You selected T2"
T15 = "You selected T2"
T19 = "You selected T2"
T22 = "You selected T2"
T25 = "You selected T2"
T30 = "You selected T2"
T32 = "You selected T2"
T34 = "You selected T2"
T35 = "You selected T2"
T36 = "You selected T2"
T37 = "You selected T2"
T38 = "You selected T2"
T39 = "You selected T2"
T40 = "You selected T2"
T41 = "You selected T2"
T44 = "You selected T2"
D = "You selected T2"
E = "You selected T2"
F = "You selected T2"
G = "You selected T2"
H = "You selected T2"
I = "You selected T2"
K = "You selected T2"
M = "You selected T2"
N = "You selected T2"
P = "You selected T2"
Q = "You selected T2"
R = "You selected T2"
S = "You selected T2"
T = "You selected T2"
Y = "You selected T2"


TARGET_LIST = [
    "T2", "T4", "T5", "T6",
    "T7", "T8", "T9", "T11",
    "T15", "T19", "T22", "T25",
    "T30", "T32", "T34", "T35",
    "T36", "T37", "T38", "T39",
    "T40", "T41", "T44",
    "D", "E", "F", "G",
    "H", "I", "K", "M",
    "N", "P", "Q", "R",
    "S", "T", "Y"]

def password():
    password = raw_input("PASSWORD? ")
    if password == "suckit":
        print "WELCOME TO R500 TARGET SELECTION"
    else:
        print "INCORRECT PASSWORD"
        return None

def tselect():
    target = raw_input("TYPE TARGET NUMBER: ")
    if target == TARGET_LIST[0]:
        print TARGET_LIST[0]
        sleep(1)
        T2()
        tselect()                    #I know you said not to call a function in its self because of memory
    elif target == TARGET_LIST[1]:   #But I don't know how to make it work without doing so.... yet.
        print TARGET_LIST[1]
        sleep(1)
        T4()
        tselect()




password()
tselect()



