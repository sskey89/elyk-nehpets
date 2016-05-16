from time import sleep
from winsound import Beep

print " _____    ______     _____      _____ "
print "|  _  |  |  ____|   /  _  \    /  _  \ "
print "| | / /  | |____   |  / \  |  |  / \  | "
print "| | \ \   \____ \  |  | |  |  |  | |  | "
print "| |  | |  ____| |  |  \_/  |  |  \_/  | "
print "|_|  |_| |______/   \_____/    \_____/ "


def T2():
    T2 = Beep(500, 500)  # This will be the function to call the servo to move


def T4():
    T4 = Beep(800, 500)  # Same


def T5():
    T5 = Beep(800, 500)


def T6():
    T6 = Beep(800, 500)


def T7():
    T7 = Beep(800, 500)


def T8():
    T8 = Beep(800, 500)


def T9():
    T9 = Beep(800, 500)


def T11():
    T11 = Beep(800, 500)


def T15():
    T15 = Beep(800, 500)


def T19():
    T19 = Beep(800, 500)


def T22():
    T22 = Beep(800, 500)


def T25():
    T25 = Beep(800, 500)


def T30():
    T30 = Beep(800, 500)


def T32():
    T32 = Beep(800, 500)


def T34():
    T34 = Beep(800, 500)


def T35():
    T35 = Beep(800, 500)


def T36():
    T36 = Beep(800, 500)


def T37():
    T37 = Beep(800, 500)


def T38():
    T38 = Beep(800, 500)


def T39():
    T39 = Beep(800, 500)


def T40():
    T40 = Beep(800, 500)


def T41():
    T41 = Beep(800, 500)


def T44():
    T44 = Beep(800, 500)


def D():
    D1 = Beep(800, 500)


def E():
    E1 = Beep(800, 500)


def F():
    F1 = Beep(800, 500)


def G():
    G1 = Beep(800, 500)


def H():
    H1 = Beep(800, 500)


def I():
    I1 = Beep(800, 500)


def K():
    K1 = Beep(800, 500)


def M():
    M1 = Beep(800, 500)


def N():
    N1 = Beep(800, 500)


def P():
    P1 = Beep(800, 500)


def Q():
    Q1 = Beep(800, 500)


def R():
    R1 = Beep(800, 500)


def S():
    S1 = Beep(800, 500)


def T():
    T1 = Beep(800, 500)


def Y():
    Y1 = Beep(800, 500)


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
    pword = raw_input("PASSWORD? ")
    if pword == "suckit":
        sleep(1)
        print "WELCOME TO R500 TARGET SELECTION"
    else:
        print "INCORRECT PASSWORD"
        sleep(1)
        return password()


def tselect():
    target = raw_input("TYPE TARGET NUMBER: ")
    if target == TARGET_LIST[0]:
        print TARGET_LIST[0]
        sleep(1)
        T2()
        tselect()  # I know you said not to call a function in its self because of memory
    elif target == TARGET_LIST[1]:  # But I don't know how to make it work without doing so.... yet.
        print TARGET_LIST[1]
        sleep(1)
        T4()
        tselect()
    elif target == TARGET_LIST[2]:
        print TARGET_LIST[2]
        sleep(1)
        T5()
        tselect()
    elif target == TARGET_LIST[3]:
        print TARGET_LIST[3]
        sleep(1)
        T6()
        tselect()
    elif target == TARGET_LIST[4]:
        print TARGET_LIST[4]
        sleep(1)
        T7()
        tselect()
    elif target == TARGET_LIST[5]:
        print TARGET_LIST[5]
        sleep(1)
        T8()
        tselect()
    elif target == TARGET_LIST[6]:
        print TARGET_LIST[6]
        sleep(1)
        T9()
        tselect()
    elif target == TARGET_LIST[7]:
        print TARGET_LIST[7]
        sleep(1)
        T11()
        tselect()
    elif target == TARGET_LIST[8]:
        print TARGET_LIST[8]
        sleep(1)
        T15()
        tselect()
    elif target == TARGET_LIST[9]:
        print TARGET_LIST[9]
        sleep(1)
        T19()
        tselect()
    elif target == TARGET_LIST[10]:
        print TARGET_LIST[10]
        sleep(1)
        T22()
        tselect()
    elif target == TARGET_LIST[11]:
        print TARGET_LIST[11]
        sleep(1)
        T25()
        tselect()
    elif target == TARGET_LIST[12]:
        print TARGET_LIST[12]
        sleep(1)
        T30()
        tselect()
    elif target == TARGET_LIST[13]:
        print TARGET_LIST[13]
        sleep(1)
        T32()
        tselect()
    elif target == TARGET_LIST[14]:
        print TARGET_LIST[14]
        sleep(1)
        T34()
        tselect()
    elif target == TARGET_LIST[15]:
        print TARGET_LIST[15]
        sleep(1)
        T35()
        tselect()
    elif target == TARGET_LIST[16]:
        print TARGET_LIST[16]
        sleep(1)
        T36()
        tselect()
    elif target == TARGET_LIST[17]:
        print TARGET_LIST[17]
        sleep(1)
        T37()
        tselect()
    elif target == TARGET_LIST[18]:
        print TARGET_LIST[18]
        sleep(1)
        T38()
        tselect()
    elif target == TARGET_LIST[19]:
        print TARGET_LIST[19]
        sleep(1)
        T39()
        tselect()
    elif target == TARGET_LIST[20]:
        print TARGET_LIST[20]
        sleep(1)
        T40()
        tselect()
    elif target == TARGET_LIST[21]:
        print TARGET_LIST[21]
        sleep(1)
        T41()
        tselect()
    elif target == TARGET_LIST[22]:
        print TARGET_LIST[22]
        sleep(1)
        T44()
        tselect()
    elif target == TARGET_LIST[23]:
        print TARGET_LIST[19]
        sleep(1)
        D()
        tselect()
    elif target == TARGET_LIST[24]:
        print TARGET_LIST[24]
        sleep(1)
        E()
        tselect()
    elif target == TARGET_LIST[25]:
        print TARGET_LIST[25]
        sleep(1)
        F()
        tselect()
    elif target == TARGET_LIST[26]:
        print TARGET_LIST[26]
        sleep(1)
        G()
        tselect()
    elif target == TARGET_LIST[27]:
        print TARGET_LIST[27]
        sleep(1)
        H()
        tselect()
    elif target == TARGET_LIST[28]:
        print TARGET_LIST[28]
        sleep(1)
        I()
        tselect()
    elif target == TARGET_LIST[29]:
        print TARGET_LIST[29]
        sleep(1)
        K()
        tselect()
    elif target == TARGET_LIST[30]:
        print TARGET_LIST[30]
        sleep(1)
        M()
        tselect()
    elif target == TARGET_LIST[31]:
        print TARGET_LIST[31]
        sleep(1)
        N()
        tselect()
    elif target == TARGET_LIST[32]:
        print TARGET_LIST[32]
        sleep(1)
        P()
        tselect()
    elif target == TARGET_LIST[33]:
        print TARGET_LIST[33]
        sleep(1)
        Q()
        tselect()
    elif target == TARGET_LIST[34]:
        print TARGET_LIST[34]
        sleep(1)
        R()
        tselect()
    elif target == TARGET_LIST[35]:
        print TARGET_LIST[35]
        sleep(1)
        S()
        tselect()
    elif target == TARGET_LIST[36]:
        print TARGET_LIST[36]
        sleep(1)
        T()
        tselect()
    elif target == TARGET_LIST[37]:
        print TARGET_LIST[37]
        sleep(1)
        Y()
        tselect()
    else:
        print "Invalid Target"
        tselect()


password()
tselect()
