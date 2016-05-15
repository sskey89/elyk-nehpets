
#This line is a test for GitHub or is it?
# Targets are listed as T2, T4, T5, or R,S,T,U, ect...

T2 = "Servo Input for Servo1X and Servo2Y T2 "
T4 = "Servo Input for Servo1X and Servo2Y T4"

#Simple Login
def var_fun():
    '''Lets explore variable types and how to minipulate strings'''

    i = 2;       #This is an integer, numbers that don't have decimals
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

    str = "Steve is dumb."

    dynamic_str = "I know for a fact that %s" % str #Dynamiclly insert str into dynamic_str

    print dynamic_str

    str2 = "Kyle is awesome."

    #Repeat

    dynamic_str = "I know for a fact that %s" % str2 #Dynamiclly insert str into dynamic_str
    print dynamic_str

    pass #If you are not returning anything then use a pass

def test():
    print "PAS-22 Control"
    password = raw_input("Password? ").lower()
    if password == "suckit":
        print "Welcome"
    else:
        print "Try again"
        test()

#Target Selection Process

def tselect():
    print "Tagret Selection"
    target = raw_input("Type in a Target Number:").lower()
    if target == "T2" or target == "t2":
         print T2
         return T2
    elif target == "T4" or target == "t4":
        print T4
        return T4

    else:
        print "Not a Valid Targrt"
        tselect()

#This is a trick used to only call what is below when you are directly calling this file, and not importing it...
if __name__ == "__main__":

    var_fun()   #Call the var_fun function
    test()      #Call the test function
    tselect()   #Call tselect function

