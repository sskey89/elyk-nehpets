from time import sleep
from winsound import Beep

def title():

    title_str = " _____    ______     _____      _____ "\
                "|  _  |  |  ____|   /  _  \    /  _  \ "\
                "| | / /  | |____   |  / \  |  |  / \  | "\
                "| | \ \   \____ \  |  | |  |  |  | |  | "\
                "| |  | |  ____| |  |  \_/  |  |  \_/  | "\
                "|_|  |_| |______/   \_____/    \_____/ "

    return title_str


def servo_motion(x, y):
    Beep(x, y)
    pass

#Use A Dictionary instead of a list. The Key is the target name, the value is a tupple of coordinates...
def get_targets():
    return {"T2": (500,500),
               "T4": (800,500),
               "T5": (800,500),
               "T6": (800,500),
               "T7": (800,500),
               "T8": (800,500),
               "T9": (800,500),
               "T11": (800,500),
               "T15": (800,500),
               "T19": (800,500),
               "T22": (800,500),
               "T25": (800,500),
               "T30": (800,500),
               "T32": (800,500),
               "T34": (800,500),
               "T35": (800,500),
               "T36": (800,500),
               "T37": (800,500),
               "T38": (800,500),
               "T39": (800,500),
               "T40": (800,500),
               "T41": (800,500),
               "T44": (800,500),
               "D": (800,500),
               "E": (800,500),
               "F": (800,500),
               "G": (800,500),
               "H": (800,500),
               "I": (800,500),
               "K": (800,500),
               "M": (800,500),
               "N": (800,500),
               "P": (800,500),
               "Q": (800,500),
               "R": (800,500),
               "S": (800,500),
               "T": (800,500),
               "Y": (800,500)
               }

def password():
    pword = raw_input("PASSWORD? ")
    if pword == "suckit":
        sleep(1)
        print "WELCOME TO R500 TARGET SELECTION"
    else:
        print "INCORRECT PASSWORD"
        sleep(1)
        return password()


def tselect():
    target_data = get_targets()     # get the dictionary of targets and coordinates
    target_list = target_data.keys() #Get a list of the keys of the dict. This is a list of valid targets.
    target = raw_input("TYPE TARGET NUMBER: ")

    #Make a case to gracefully exit the program
    if target.upper == "EXIT" or target.upper == "QUIT":
        return False

    #Check if given target is in the target list
    if target.upper() in target_list:
        print target
        #Get the coordinates for a target
        coords = target_data[target]
        sleep(1) #Not sure why you want to sleep here...

        #Set variables for your x and y coordinates... dont really need to do this but its easier to read the code
        x_coord = coords[0]
        y_coord = coords[1]

        #Call servo motion given the coordinates
        servo_motion(x_coord, y_coord)
    else:
        print "Invalid Target"
        pass

    return True

if __name__ == "__main__":
    print title()
    password()
    run_tselect = True
    #This loop will run as long as run_tselect = True
    while run_tselect:
        run_tselect = tselect()
        pass

