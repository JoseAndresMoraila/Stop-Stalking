import ttkbootstrap as tb
from ttkbootstrap.constants import *
from app import Principal  # Asegúrate de que el nombre del archivo coincida con tu módulo
import sys
import os

def main():
    try:
        # Hace que las excepciones y print no salgan en consola pero usarse cuando se vaya a hacer exe
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        root = tb.Window(themename="superhero")
        root.title("Stop Stalking")

        if os.name == 'posix':
            logo = tb.PhotoImage(file="img/StopStalking.png")
            root.iconphoto(True, logo)
        else:
            root.iconbitmap('img/StopStalking.ico')

        app = Principal(root=root)  # Instancia Principal
        root.mainloop()  # Inicia el loop de eventos de Tkinter

    except:
        pass
if __name__ == '__main__':
    main()
