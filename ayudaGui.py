import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os

class ayudaClase():
    def __init__(self) -> None:
        self.windowAyuda = tb.Toplevel()
        if os.name == 'nt':self.windowAyuda.iconbitmap('img/StopStalking.ico')
        self.windowAyuda.title("Ayuda JSONs")
        self.windowAyuda.withdraw()

        self.Widgets()

        self.windowAyuda.deiconify()
        self.windowAyuda.lift()

    def Widgets(self):
        fatherFramem = tb.Frame(self.windowAyuda)
        fatherFramem.grid(row=0, column=0)
        self.windowAyuda.grid_rowconfigure(0, weight=1)
        self.windowAyuda.grid_columnconfigure(0, weight=1)

        paso1 = '1.- En Instagram ve a Centro de Cuentas'
        labelPaso1 = tb.Label(fatherFramem, text=paso1)
        labelPaso1.grid(row=0, column=0, sticky=NSEW)
        fatherFramem.grid_columnconfigure(0, weight=1)
        fatherFramem.grid_rowconfigure(0, weight=1)

        paso2 = '2.- En Comfiguración de Cuenta pincha en Tu Informción y Permisos'
        labelPaso2 = tb.Label(fatherFramem, text=paso2)
        labelPaso2.grid(row=1, column=0, sticky=NSEW)
        fatherFramem.grid_rowconfigure(1, weight=1)

        paso3 = '3.- Pincha en Descargar o Transferir Información y seleccionas tú cuenta de Instagram'
        labelPaso3 = tb.Label(fatherFramem, text=paso3)
        labelPaso3.grid(row=2, column=0, sticky=NSEW)    
        fatherFramem.grid_rowconfigure(2, weight=1)

        paso4 = '4.- Pica en Parte De Tu Información y después en la sección Conexiones le picas a\nSeguidores y Seguidos'
        labelPaso4 = tb.Label(fatherFramem, text=paso4)
        labelPaso4.grid(row=3, column=0, sticky=NSEW)    
        fatherFramem.grid_rowconfigure(3, weight=1)

        paso5 = '5.- Le puedes picar a descargar en dispositivo o transferir a la nube.'
        labelPaso5 = tb.Label(fatherFramem, text=paso5)
        labelPaso5.grid(row=4, column=0, sticky=NSEW)    
        fatherFramem.grid_rowconfigure(4, weight=1)

        paso6 = '6.- Una vez hecho lo correspondiente en Rango de Fecha tienes que ponerle en Desde El Principio.\nY en Formato le tienes que poner JSON'
        labelPaso6 = tb.Label(fatherFramem, text=paso6)
        labelPaso6.grid(row=5, column=0, sticky=NSEW)
        fatherFramem.grid_rowconfigure(5, weight=1)

        paso7 = '7.- Después de haber hecho lo anterior te pedirá que ingreses tu contraseña de Instagram y ya que la ingreses\ntendrás que esperar unos minutos para que la petición de recopilación de información termine'
        labelPaso7 = tb.Label(fatherFramem, text=paso7)
        labelPaso7.grid(row=6, column=0, sticky=NSEW)
        fatherFramem.grid_rowconfigure(6, weight=1)

        paso8= '8.- Puedes volver en un tiempo a esa sección y descargar el ZIP y/o si lo mandaste a la nube lo descargas en la PC\npara que este programa lo pueda analizar'
        labelPaso8 = tb.Label(fatherFramem, text=paso8)
        labelPaso8.grid(row=7, column=0, sticky=NSEW)
        fatherFramem.grid_rowconfigure(7, weight=1)
