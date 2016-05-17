from time import sleep
# from winsound import Beep


'''Made major changes to Servo.py to reduce the amount of code needed.
    Rule of Thumb with coding: You should never have to type the same code twice.'''

def title():

    title_str = " _____    ______     _____      _____ \n"\
                "|  _  |  |  ____|   /  _  \    /  _  \ \n"\
                "| | / /  | |____   |  / \  |  |  / \  |\n"\
                "| | \ \   \____ \  |  | |  |  |  | |  | \n"\
                "| |  | |  ____| |  |  \_/  |  |  \_/  | \n"\
                "|_|  |_| |______/   \_____/    \_____/ \n"

    return title_str


def servo_motion(x, y):
    Beep(x, y)
    pass

# Use A Dictionary instead of a list. The Key is the target name, the value is a tupple of coordinates...
# Eventually you will want to save this out to a file so you can add/modify target coordinates on the fly...

def get_targets_from_txt():

    my_file = open("targets.txt", "rb") # open targets.txt, rb means read-binary mode
    data = my_file.readlines()  # Call readlines() to make a list of all the lines in the file.
    my_file.close() # We have to close the file or it can become corrupted.

    data_dict = {} # make an empty dictionary to store the data

    # Populate the dictionary... we can only do this because we know the structure of the data in targets.txt
    # We made it a comma-separated list

    for line in data:
        # First we remove the newline characters from each string, using .replace(). Replace will find every instance
        # of the first argument and replace it with the second argument. So here we are looking for every instance of
        # \n and replacing it with nothing, effectively removing it.

        line = line.replace("\n","")

        # Now we spilt the string at each comma to make a list.
        # split is method that can be used on strings. It will split the string into a list, using the argument to
        # split on. So here we are splitting the string into parts using a comma as the split point

        line_list = line.split(",")

        #Since we put the target name first, then the coordinates in the text file, we know that the first element in
        # the list will be the target and the others the coordinates.

        target = line_list[0]
        x_coord = line_list[1]
        y_coord = line_list[2]

        #Now we dynamically populate the dictionary

        data_dict[target] = [x_coord, y_coord]
        pass

    return data_dict

def update_file(filename, target_dict):
    # This function will take the given dictionary and write it to a text file

    keys = target_dict.keys() #Get all the keys of the dict

    my_file = open(filename, "wb") # Now we open the file but give "wb" to write to it

    for k in keys:
        #Turn the data into a string... see if you can figure out what I am doing here
        line = "%s, %s, %s\n" % (k, target_dict[k][0], target_dict[k][1])

        #Write the line to the file
        my_file.write(line)
        pass

    my_file.close() #close the file or it will become corrupted
    pass






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
    target = raw_input("TYPE TARGET NUMBER: ").upper() #Cast input to upper case string

    #Make a case to gracefully exit the program
    if target == "EXIT" or target == "QUIT":
        print "Quitting..."
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
    # print title()
    # password()
    # run_tselect = True
    # This loop will run as long as run_tselect = True
    # We also could have built this loop into tselect()
    # but I like it outside in case we want to use tselect a different way
    # while run_tselect:
    #     run_tselect = tselect()
    #     pass

    #Lets see the file stuff in action
    my_dict = get_targets_from_txt()

    #Lets add a couple targets
    my_dict["Kyle1"] = [100, 600]
    my_dict["Kyle2"] = [400, 500]

    #Now lets save out the file, we will use a different file name for comparison
    update_file("updated_targets.txt", my_dict)

