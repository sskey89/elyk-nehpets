__author__ = 'yeks'
import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                return "up"
        elif k=='\x1b[B':
                return "down"
        elif k=='\x1b[C':
                return "right"
        elif k=='\x1b[D':
                return "left"
        else:
                print "not an arrow key!"
                return None

def main():
        for i in range(0,20):
                get()

if __name__=='__main__':
        main()
