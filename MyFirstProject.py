
#This line is a test for GitHub or is it?
# Targets are listed as T2, T4, T5, or R,S,T,U, ect...
from time import sleep

#Simple Login
def var_fun():
    '''Lets explore variable types and how to minipulate strings'''

    i = 2      #This is an integer, numbers that don't have decimals
    n = 3.2453   #This is a float (or double), a dumber that has a decimal;
    i2 = 3      #This is another integer

    divisor = i/i2
    #two integers divided equals how many times I can evenly divide two integers. e.g 2/3 = 0
    # since two divides into three zero times.'''

    print divisor

    #But an Integer divided by a double equals a double
    div = i/n
    print div

    modulo = i%i2
    # A modulo (%) gives you the remainder of integer division. e.g. 2%3 = 2 since 2 divdies into 3 zero
    # times and has a remainder of 2.'''

    print modulo

    i = 5   #Make i equal to 5

    #repeat previous code

    divisor = i/i2  #Now 5/3 = 1 since 5 divides into 3 evenly once
    print divisor

    modulo = i%i2   #now 5%3 = 2 since 5 divides into 3 evenly once and has 2 left over

    print modulo

    #You can also dynamically print a variable by using % in the string

    print "The modulo is %d" % modulo #%d is a wildcard for the integer you specify by the % variable_name you define
    #Shoud print 'The modulo is 2'

    #this can also be done with strings

    str = "Steve is the coolest."

    dynamic_str = "I know for a fact that %s" % str #Dynamiclly insert str into dynamic_str

    print dynamic_str

    str2 = "Kyle has a beer belly."

    #Repeat

    dynamic_str = "I know for a fact that %s" % str2 #Dynamiclly insert str into dynamic_str
    print dynamic_str

    pass #If you are not returning anything then use a pass

def tupple_list_dict():
    # A tupple is an ordered list of comma separated variables that can't be edited once made
    # This tupple contains 5 elements
    my_tup = (1, 2, 3, 5, 9)
    print my_tup

    # You can reference a variable inside the tupple by order by using an index
    # Indexes start at 0
    print my_tup[0] # will print 1
    print my_tup[3] # will print 5

    # A list is the same as a tupple, but you can edit the list contents, size, etc.
    my_list = [1, 4, 9, 2, 6, 5, 8]
    print my_list

    #Replace the 9 with a 10
    my_list[2] = 10
    print my_list

    #Lists can be sorted
    my_list.sort()
    print my_list

    #You can merge lists together
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]

    list3 = list1 + list2
    print list3

    #You can append to the end of the list
    list3.append(7)
    print list3

    #You can append a list to a list
    #This literally makes list2 an element of list1 - list inception!!
    list1.append(list2)
    print list1

    #You can extend a list with another list
    #This adds the elements of list 2 to list 1 just like we did with +
    list1.extend(list2)
    print list1

    #You can pop the last variable off the list
    var = list1.pop()
    print var
    print list1

    # A Dictionary is a list of key,value pairs {key1:val1, key2:val2}
    # Since the dict is based on key,value paires, order is not important

    car_dict1 = {"make":"Hyundai", "model":"Elantra", "color":"Silver", "milage":35000, "hasBluetooh":True}
    car_dict2 = {"make":"Chevy", "model":"Cavalier", "color":"Blue", "milage":195000, "hasBluetooth":False}
    print car_dict1
    print car_dict2

    #You can get a value by key, just like indexing for lists and tupples
    print car_dict1["make"] #Prints Hyundai
    print car_dict2["make"] #Prints Chevy

    #You can also add or edit key,value pairs the same way
    car_dict1["milage"] = 40000

    print car_dict1

    car_dict1["insured"] = True
    car_dict2["insured"] = False

    print car_dict1
    print car_dict2

    #You can get a list of all the keys in a dict
    d_keys =  car_dict1.keys()

    # Now you could use a FOR loop to display all the values in a dict
    # I will do another function that explains loops in detail
    for k in d_keys:
        value = car_dict1[k]
        print "%s: %s" % (k, value)
        pass


def test():
    print "PAS-22 Control"
    password = raw_input("Password? ").lower()
    if password == "suckit":
        sleep(3)
        print "Welcome"
    else:
        print "Try again"
        test()

#Target Selection Process

def tselect():

    T2 = "Servo Input for Servo1X and Servo2Y T2 "
    T4 = "Servo Input for Servo1X and Servo2Y T4"

    print "Tagret Selection"
    target = raw_input("Type in a Target Number:")
    if target == "t2": # target will never == "T2" since you called .lower() above
         print T2
         return T2
    elif target == "t4":
        print T4
        return T4

    else:
        print "Not a Valid Targrt"
        return None
        # tselect() Try not to call a function inside of itself. Its called recursion and can waste memory

def stuff()
    prices = {
        "banana" : 4,
        "apple" : 2,
        "orange" : 1.5,
        "pear" : 3
        }
    stock = {
        "banana" : 6,
        "apple" : 0,
        "orange" : 32,
        "pear" : 15
        }
    for key in prices:
        print key
        print "price: %d" % prices[key]
        print "stock: %d" % stock[key]


#This is a trick used to only call what is below when you are directly calling this file, and not importing it...
if __name__ == "__main__":

    #var_fun()   #Call the var_fun function
    #test()
    #Call the test function
    #tselect()   #Call tselect function
stuff()