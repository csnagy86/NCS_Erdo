from tkinter import Tk
from ncs_game import NCSErdoAlkalmazas

def main():
    root = Tk()
    app = NCSErdoAlkalmazas(root)
    root.mainloop()

if __name__ == "__main__":
    main()