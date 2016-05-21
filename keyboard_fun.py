__author__ = 'yeks'
import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        # print ord(k)
        if k=='\x1b':
            k = inkey()
            if k=="[":
                k = inkey()
                if k == "A":
                    return "up"
                elif k=='B':
                    return "down"
                elif k=='C':
                    return "right"
                elif k=='D':
                    return "left"
        elif ord(k) == 3:
            exit(0)
            pass
        else:
            return k


def main():
        for i in range(0,20):
                print get()

if __name__=='__main__':
        main()