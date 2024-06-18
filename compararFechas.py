import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk
import json
from ttkbootstrap.dialogs import Messagebox
import datetime
from ttkbootstrap.tableview import Tableview
from Herramientas import Funcionalidades
import instaloader
import os
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError, NameResolutionError

class ClaseVentanaCompararSeguidores():
    def __init__(self) -> None:
        self.ventananaCompararSeguidores = tb.Toplevel()
        if os.name == 'nt':self.ventananaCompararSeguidores.iconbitmap('img/StopStalking.ico')
        self.ventananaCompararSeguidores.title("Comparar seguidores entre fechas")
        self.ventananaCompararSeguidores.withdraw()

        self.fatherFrame = tb.Frame(self.ventananaCompararSeguidores)
        self.fatherFrame.grid(row=0, column=0)
        self.ventananaCompararSeguidores.grid_rowconfigure(0, weight=1)
        self.ventananaCompararSeguidores.grid_columnconfigure(0, weight=1)

        self.Widgets()

        self.ventananaCompararSeguidores.update_idletasks()
        self.ventananaCompararSeguidores.deiconify()
        self.ventananaCompararSeguidores.lift()
        self.ventananaCompararSeguidores.attributes("-topmost", True)

    def Widgets(self):
        stilo = tb.Style()
        stilo.configure('Comparacion.TButton', font=('Arial', 15), background='#FF5733', bordercolor='#FF5733', borderwidth=0)
        stilo.configure('VerLA.TButton', font=('Arial', 10), background='#FF3368', bordercolor='#FF3368', borderwidth=0)
        stilo.map('VerLA.TButton',background=[("active", "#B92C51")]) #Esto hace que al apsar el mouse por arriba cambie de color
        stilo.map('Comparacion.TButton',background=[("active", "#C93F21")])

        labelSeguidoresFecha1 = tb.Label(self.fatherFrame, text='Selecciona archivo de seguidores de fecha pasada')
        labelSeguidoresFecha1.grid(row=0, column=0, sticky=NSEW, pady=15)
        self.fatherFrame.grid_columnconfigure(0, weight=1)
        self.fatherFrame.grid_rowconfigure(0, weight=1)

        buttonSeguidores1 = tb.Button(self.fatherFrame, text='Seleccionar .json de seguidores pasado', command=self.Elegir_Json_Followers_Longevo, style="Comparacion.TButton")
        buttonSeguidores1.grid(row=1, column=0, pady=15)
        self.fatherFrame.grid_rowconfigure(1, weight=1)

        labelSeguidoresFecha2 = tb.Label(self.fatherFrame, text='Selecciona archivo de seguidores actual')
        labelSeguidoresFecha2.grid(row=2, column=0, sticky=NSEW, pady=15)
        self.fatherFrame.grid_rowconfigure(2, weight=1)

        buttonSeguidores2 = tb.Button(self.fatherFrame, text='Seleccionar .json de seguidores más actual', command=self.Elegir_Json_Followers_Actual, style="Comparacion.TButton")
        buttonSeguidores2.grid(row=3, column=0, pady=15)
        self.fatherFrame.grid_rowconfigure(3, weight=1)

        buttonVerResultados = tb.Button(self.fatherFrame, text='Ver seguidores entre fechas', style="VerLA.TButton", command=self.Comparar_Jsons)
        buttonVerResultados.grid(row=4, column=0)
        self.fatherFrame.grid_rowconfigure(4, weight=1)

        consejo = 'CUIDADO: Si seleccionas el json de una fecha pasada en el actual y el json actual en la pasada los datos saldrán al revés\nOJO: Si seleccionas el mismo archivo para pasado y actual no saldrá nada'
        labelConsejo = tb.Label(self.fatherFrame, text=consejo)
        labelConsejo.grid(row=5, column=0, sticky=NSEW)
        self.fatherFrame.grid_rowconfigure(5, weight=1)

    def Elegir_Json_Followers_Longevo(self):
        self.ventananaCompararSeguidores.iconify()
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo seguidores',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.dataFollowers = json.load(file)

                values = []
                hrefFollowers= []
                self.followersTimestampDicLongevo = {}

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for entry in self.dataFollowers:
                        for string_data in entry["string_list_data"]:
                            # Extraer el valor de "value" y añadirlo 
                            values.append(string_data["value"])
                            hrefFollowers.append(string_data["href"])
                            ususario = string_data["value"]
                            tiempo = string_data["timestamp"]
                            self.followersTimestampDicLongevo[ususario] = tiempo

                    self.followersLongevoTuple = tuple(values)
                    self.followersHrefLongevoTuple = tuple(hrefFollowers)
                except: Messagebox.show_error("Archivo incorrecto", "Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")

            except json.JSONDecodeError:
                Messagebox.show_error(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")
        self.ventananaCompararSeguidores.deiconify()

    def Elegir_Json_Followers_Actual(self):
        self.ventananaCompararSeguidores.iconify()
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo seguidores',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.dataFollowers = json.load(file)

                values = []
                hrefFollowers= []
                self.followersTimestampDicActual = {}

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for entry in self.dataFollowers:
                        for string_data in entry["string_list_data"]:
                            # Extraer el valor de "value" y añadirlo 
                            values.append(string_data["value"])
                            hrefFollowers.append(string_data["href"])
                            ususario = string_data["value"]
                            tiempo = string_data["timestamp"]
                            self.followersTimestampDicActual[ususario] = tiempo

                    self.followersActualTuple = tuple(values)
                    self.followersHrefActualTuple = tuple(hrefFollowers)
                except: Messagebox.show_error("Archivo incorrecto", "Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")

            except json.JSONDecodeError:
                Messagebox.show_error(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")
        self.ventananaCompararSeguidores.deiconify()

    def Comparar_Jsons(self):
        try:
            longevoSet = set(self.followersLongevoTuple)
            actualSet = set(self.followersActualTuple)
            
            # Seguidores que dejaron de seguirte (están en longevo pero no en actual)
            dejaronDeSeguir = longevoSet - actualSet
            dejaronDeSeguirList = [[seguidor] for seguidor in dejaronDeSeguir]

            # Seguidores nuevos (están en actual pero no en longevo)
            nuevosSeguidores = actualSet - longevoSet

            # Crear lista para almacenar los resultados para la interfaz gráfica
            valuesD = []
            for seguidor in self.followersActualTuple:
                if seguidor not in self.followersLongevoTuple:
                    timestamp = self.followersTimestampDicActual.get(seguidor, None)
                    fechaLegible = Funcionalidades.ConvertirFecha(timestamp) if timestamp else 'Desconocido'
                    valuesD.append((seguidor, fechaLegible))

            # Suponiendo que valuesD es tu lista de conjuntos que contiene usuarios y fechas
            usuarioFecha = [[usuario, fecha] for usuario, fecha in valuesD]

            self.ventananaCompararSeguidores.iconify()
            ventanaTablasSeguidoresOno = tb.Toplevel()
            if os.name == 'nt':ventanaTablasSeguidoresOno.iconbitmap('img/StopStalking.ico')
            ventanaTablasSeguidoresOno.title("Ver comparaciones")
            ventanaTablasSeguidoresOno.withdraw()
            frameTablasNuevosViejos = tb.Frame(ventanaTablasSeguidoresOno)
            frameTablasNuevosViejos.grid(row=0, column=0, sticky=NSEW)
            ventanaTablasSeguidoresOno.grid_rowconfigure(0, weight=1)
            ventanaTablasSeguidoresOno.grid_columnconfigure(0, weight=1)

            self.tablaDejoDeSeguir = Tableview(frameTablasNuevosViejos, coldata=['Usuario que te dejó de seguir'], rowdata=dejaronDeSeguirList, searchable=True, autofit=True)
            self.tablaDejoDeSeguir.align_column_center(cid=0)
            self.tablaDejoDeSeguir.align_heading_center(cid=0)
            self.tablaDejoDeSeguir.grid(row=0, column=0, sticky=NSEW)
            frameTablasNuevosViejos.grid_rowconfigure(0, weight=1)
            frameTablasNuevosViejos.grid_columnconfigure(0, weight=1)
            buttonVerDejoDeSeguir = tb.Button(frameTablasNuevosViejos, text='Ver usuario que te dejó de seguir', command=self.Abrir_Ventana_No_Te_Sigue)
            buttonVerDejoDeSeguir.grid(row=1, column=0)
            frameTablasNuevosViejos.grid_rowconfigure(1, weight=0)

            self.tablaNuevosSeguidores = Tableview(frameTablasNuevosViejos, coldata=['Nuevos seguidores', 'Fecha que te empezó a seguir'], rowdata=usuarioFecha, searchable=True, autofit=True)
            self.tablaNuevosSeguidores.align_column_center(cid=0)
            self.tablaNuevosSeguidores.align_heading_center(cid=0)
            self.tablaNuevosSeguidores.align_column_center(cid=1)
            self.tablaNuevosSeguidores.align_heading_center(cid=1)
            self.tablaNuevosSeguidores.grid(row=0, column=1, sticky=NSEW)
            frameTablasNuevosViejos.grid_columnconfigure(1, weight=1)
            buttonVerNuevoSeguidor = tb.Button(frameTablasNuevosViejos, text='Ver seguidor nuevo', command=self.Abrir_Ventana_Nuevo_Seguidor)
            buttonVerNuevoSeguidor.grid(row=1, column=1)
            frameTablasNuevosViejos.grid_columnconfigure(1, weight=0)

            self.imgCacheDejoDeSeguir = {}
            self.imgCacheSeguidorNuevo = {}

            ventanaTablasSeguidoresOno.update_idletasks()
            ventanaTablasSeguidoresOno.deiconify()
            ventanaTablasSeguidoresOno.lift()
            
            #Cuando se cierra la ventana que muestra los resultados se vuelve a mostrar la anterior
            ventanaTablasSeguidoresOno.protocol("WM_DELETE_WINDOW", lambda:self.Ventana_Destruida(ventanaTablasSeguidoresOno))

        except:
            self.ventananaCompararSeguidores.iconify()
            Messagebox.show_error(title="Error", message="Selecciona los archivos correspondientes")
            self.ventananaCompararSeguidores.deiconify()
    
    def Ventana_Destruida(self, ventana):
        self.ventananaCompararSeguidores.deiconify()
        ventana.destroy()

    def Abrir_Ventana_No_Te_Sigue(self):
        tableRows = self.tablaDejoDeSeguir.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.followersHrefLongevoTuple:
            if user in href:
                enlace = href
                break
        
        if enlace is None:
            Messagebox.show_error(title='Error', message='No se encontró el enlace para el usuario seleccionado.')
            return

        windowVer = tb.Toplevel()
        if os.name == 'nt':windowVer.iconbitmap('img/StopStalking.ico')
        windowVer.title("Ver a: " + user)
        windowVer.withdraw()

        try:
            if not Funcionalidades.check_internet_connection():
                windowVer.iconify()
                Messagebox.show_error(title='Error en conexión', message='No se detectó conexión a internet. Por favor, verifica tu conexión.')
                windowVer.deistroy()
                return
            
            if user in self.imgCacheDejoDeSeguir:
                img = self.imgCacheDejoDeSeguir[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheDejoDeSeguir[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheDejoDeSeguir[user] = None

            if img:
                self.img_tk = ImageTk.PhotoImage(img)
            else:
                self.img_tk = None
                windowVer.iconify()
                Messagebox.show_warning(title='Advertencia', message='No se pudo cargar la imagen del perfil.')
                windowVer.deiconify()

        except instaloader.exceptions.ProfileNotExistsException:
            windowVer.iconify()
            Messagebox.show_error(title='Perfil no existe', message='El perfil seleccionado no existe')
            windowVer.deiconify()
            self.img_tk = None
        except (requests.exceptions.ConnectionError, instaloader.exceptions.ConnectionException):
            windowVer.iconify()
            Messagebox.show_error(title='Error en conexión', message='Hubo un error en la conexión a internet')
            windowVer.deiconify()
            self.img_tk = None
        except (MaxRetryError, NewConnectionError, NameResolutionError):
            windowVer.iconify()
            Messagebox.show_error(title='Error en conexión', message='Hubo un error en la conexión a internet')
            windowVer.deiconify()
            self.img_tk = None
        except:
            windowVer.iconify()
            Messagebox.show_error(title='Error', message='Hubo algún error')
            windowVer.deiconify()
            self.img_tk = None

        if self.img_tk:
            labelImagen = tb.Label(windowVer, image=self.img_tk)
            labelImagen.grid(row=0, column=0, sticky=NSEW)
            windowVer.grid_columnconfigure(0, weight=1)
            windowVer.grid_rowconfigure(0, weight=1)

        labelEnlace = tb.Label(windowVer, text=enlace, cursor="hand2")
        labelEnlace.grid(row=0, column=1, sticky=NSEW)
        windowVer.grid_columnconfigure(1, weight=1)
        labelEnlace.bind("<Button-1>", lambda event, url=enlace: Funcionalidades.AbrirEnlace(event, url))

        windowVer.update_idletasks()
        windowVer.deiconify()
        windowVer.lift()

    def Abrir_Ventana_Nuevo_Seguidor(self):
            tableRows = self.tablaNuevosSeguidores.get_rows(selected=True)
            for row in tableRows:
                user = row.values[0]
            
            # Find the correct href for the user
            enlace = None
            for href in self.followersHrefActualTuple:
                if user in href:
                    enlace = href
                    break
            
            if enlace is None:
                Messagebox.showe_rror(title='Error', message='No se encontró el enlace para el usuario seleccionado.')
                return

            windowVer = tb.Toplevel()
            if os.name == 'nt':windowVer.iconbitmap('img/StopStalking.ico')
            windowVer.title("Ver a: " + user)
            windowVer.withdraw()

            try:
                if not Funcionalidades.check_internet_connection():
                    windowVer.iconify()
                    Messagebox.show_error(title='Error en conexión', message='No se detectó conexión a internet. Por favor, verifica tu conexión.')
                    windowVer.deistroy()
                    return

                if user in self.imgCacheSeguidorNuevo:
                    img = self.imgCacheSeguidorNuevo[user]
                else:
                    bot = instaloader.Instaloader()
                    profile = instaloader.Profile.from_username(bot.context, user)
                    img = Funcionalidades.RequestImg(profile.profile_pic_url)
                    if img:
                        img = img.resize((500, 500), Image.LANCZOS)
                        self.imgCacheSeguidorNuevo[user] = img
                        self.img_tk = ImageTk.PhotoImage(img)
                    else:
                        self.imgCacheSeguidorNuevo[user] = None

                if img:
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.img_tk = None
                    windowVer.iconify()
                    Messagebox.show_warning(title='Advertencia', message='No se pudo cargar la imagen del perfil.')
                    windowVer.deiconify()

            except instaloader.exceptions.ProfileNotExistsException:
                windowVer.iconify()
                Messagebox.show_error(title='Perfil no existe', message='El perfil seleccionado no existe')
                windowVer.deiconify()
                self.img_tk = None
            except (requests.exceptions.ConnectionError, instaloader.exceptions.ConnectionException):
                windowVer.iconify()
                Messagebox.show_error(title='Error en conexión', message='Hubo un error en la conexión a internet')
                windowVer.deiconify()
                self.img_tk = None
            except (MaxRetryError, NewConnectionError, NameResolutionError):
                windowVer.iconify()
                Messagebox.show_error(title='Error en conexión', message='Hubo un error en la conexión a internet')
                windowVer.deiconify()
                self.img_tk = None
            except:
                windowVer.iconify()
                Messagebox.show_error(title='Error', message='Hubo algún error')
                windowVer.deiconify()
                self.img_tk = None

            if self.img_tk:
                labelImagen = tb.Label(windowVer, image=self.img_tk)
                labelImagen.grid(row=0, column=0, sticky=NSEW)
                windowVer.grid_columnconfigure(0, weight=1)
                windowVer.grid_rowconfigure(0, weight=1)

            labelEnlace = tb.Label(windowVer, text=enlace, cursor="hand2")
            labelEnlace.grid(row=0, column=1, sticky=NSEW)
            windowVer.grid_columnconfigure(1, weight=1)
            labelEnlace.bind("<Button-1>", lambda event, url=enlace: Funcionalidades.AbrirEnlace(event, url))

            windowVer.update_idletasks()
            windowVer.deiconify()
            windowVer.lift()
