import ttkbootstrap as tb
from ttkbootstrap.constants import *
import json
from tkinter import messagebox, filedialog
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from urllib3.exceptions import MaxRetryError, NewConnectionError, NameResolutionError
import requests
from ttkbootstrap.tableview import Tableview
from Herramientas import Funcionalidades
import instaloader
import os

class ClaseCompararJsonsOtrosUsers():
    def __init__(self) -> None:
        self.windowOtrosUsersJson = tb.Toplevel()
        if os.name == 'nt':self.windowOtrosUsersJson.iconbitmap('img/StopStalking.ico')
        self.windowOtrosUsersJson.title("Comparar JSONs de otros users")
        self.windowOtrosUsersJson.withdraw()

        self.Widgets()

        self.windowOtrosUsersJson.update_idletasks()
        self.windowOtrosUsersJson.deiconify()
        self.windowOtrosUsersJson.lift()

    def Widgets(self):
        stilo = tb.Style()
        stilo.configure('Comparacion.TButton', font=('Arial', 15), background='#FF5733', bordercolor='#FF5733', borderwidth=0)
        stilo.configure('VerLA.TButton', font=('Arial', 10), background='#FF3368', bordercolor='#FF3368', borderwidth=0)
        stilo.map('VerLA.TButton',background=[("active", "#B92C51")]) #Esto hace que al apsar el mouse por arriba cambie de color
        stilo.map('Comparacion.TButton',background=[("active", "#C93F21")])

        self.fatherFrame = tb.Frame(self.windowOtrosUsersJson)
        self.fatherFrame.grid(row=0, column=0, sticky=NSEW)
        self.windowOtrosUsersJson.grid_columnconfigure(0, weight=1)
        self.windowOtrosUsersJson.grid_rowconfigure(0, weight=1)

        labelSeguidoresFecha1 = tb.Label(self.fatherFrame, text='Selecciona archivo de espiado de fecha pasada')
        labelSeguidoresFecha1.grid(row=0, column=0, sticky=NSEW, pady=15)
        self.fatherFrame.grid_columnconfigure(0, weight=1)
        self.fatherFrame.grid_rowconfigure(0, weight=1)

        buttonSeguidores1 = tb.Button(self.fatherFrame, text='Seleccionar .json pasado', style="Comparacion.TButton", command=self.Elegir_Json_User_Longevo)
        buttonSeguidores1.grid(row=1, column=0, pady=15)
        self.fatherFrame.grid_rowconfigure(1, weight=1)

        labelSeguidoresFecha2 = tb.Label(self.fatherFrame, text='Selecciona archivo de despiado de seguidores actual')
        labelSeguidoresFecha2.grid(row=2, column=0, sticky=NSEW, pady=15)
        self.fatherFrame.grid_rowconfigure(2, weight=1)

        buttonSeguidores2 = tb.Button(self.fatherFrame, text='Seleccionar .json de espiado más actual', style="Comparacion.TButton", command=self.Elegir_Json_User_Actual)
        buttonSeguidores2.grid(row=3, column=0, pady=15)
        self.fatherFrame.grid_rowconfigure(3, weight=1)

        buttonVerLoPerdido = tb.Button(self.fatherFrame, text='Ver quién lo dejó de seguir y a quien dejó de seguir', style="VerLA.TButton", command=self.Comparar_Resultados_Perdidos)
        buttonVerLoPerdido.grid(row=4, column=0)
        self.fatherFrame.grid_rowconfigure(4, weight=1)

        buttonVerLoGanado = tb.Button(self.fatherFrame, text='Ver quién lo empezó a seguir y a quién emepezó a seguir', style="VerLA.TButton", command=self.Comparar_Resultados_Ganados)
        buttonVerLoGanado.grid(row=5, column=0, pady=10)
        self.fatherFrame.grid_rowconfigure(5, weight=1)

        consejo = 'CUIDADO: Si seleccionas el json de una fecha pasada en el actual y el json actual en la pasada los datos saldrán al revés\nOJO: Si seleccionas el mismo archivo para pasado y actual no saldrá nada'
        labelConsejo = tb.Label(self.fatherFrame, text=consejo)
        labelConsejo.grid(row=6, column=0, sticky=NSEW)
        self.fatherFrame.grid_rowconfigure(6, weight=1)

    def Elegir_Json_User_Longevo(self):
        self.windowOtrosUsersJson.iconify()
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.longevoDataFollowers = json.load(file)

                self.longevoFollowers = []
                self.longevoFollowees = []
                self.longevoHrefFollowers= []
                self.longevoHrefFollowees = []

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for entry in self.longevoDataFollowers["followers"]:
                        self.longevoFollowers.append(entry["username"])
                        self.longevoHrefFollowers.append(entry["link"])

                    for entry in self.longevoDataFollowers["followees"]:
                        self.longevoFollowees.append(entry["username"])
                        self.longevoHrefFollowees.append(entry["link"])

                except: messagebox.showerror("Archivo incorrecto", "Selecciona el acrhivo correcto, deber ser el que guardaste al comparar seguidores y seguidos de usuario anteriormente")

            except json.JSONDecodeError:
                messagebox.showerror(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser el que guardaste al comparar seguidores y seguidos de usuario anteriormente")
        self.windowOtrosUsersJson.deiconify()

    def Elegir_Json_User_Actual(self):
        self.windowOtrosUsersJson.iconify()
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.actualDataFollowers = json.load(file)

                self.actualFollowers = []
                self.actualFollowees = []
                self.actualHrefFollowers= []
                self.actualHrefFollowees = []

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for entry in self.actualDataFollowers["followers"]:
                        self.actualFollowers.append(entry["username"])
                        self.actualHrefFollowers.append(entry["link"])

                    for entry in self.actualDataFollowers["followees"]:
                        self.actualFollowees.append(entry["username"])
                        self.actualHrefFollowees.append(entry["link"])

                except: messagebox.showerror("Archivo incorrecto", "Selecciona el acrhivo correcto, deber ser el que guardaste al comparar seguidores y seguidos de usuario más actual")

            except json.JSONDecodeError:
                messagebox.showerror(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser el que guardaste al comparar seguidores y seguidos de usuario más actual")
        self.windowOtrosUsersJson.deiconify()

    def Comparar_Resultados_Perdidos(self):
        try:
            longevoSeguidoresSet = set(self.longevoFollowers)
            longevoSeguidosSet = set(self.longevoFollowees)
            actualSeguidoresSet = set(self.actualFollowers)
            actualSeguidosSet = set(self.actualFollowees)

            #Dejaron de seguir:
            dejaronDeSeguirSet = longevoSeguidoresSet - actualSeguidoresSet
            #Dejó de seguir:
            dejoDeSeguirSet = longevoSeguidosSet - actualSeguidosSet

            #Se convierte en una lista para evitar no orden:
            dejaronDeSeguirList = [[seguidorPerdido]for seguidorPerdido in dejaronDeSeguirSet]
            dejoDeSeguirList =[[yaNoSigue] for yaNoSigue in dejoDeSeguirSet]

            #Se muestra la ventana con tablas e información
            ventanaResultadosPerdidos = tb.Toplevel()
            if os.name == 'nt':ventanaResultadosPerdidos.iconbitmap('img/StopStalking.ico')
            ventanaResultadosPerdidos.title('Ver usuarios que dejaron y dejó de seguir el espiado')
            ventanaResultadosPerdidos.withdraw()

            frameTablasPerdidos = tb.Frame(ventanaResultadosPerdidos)
            frameTablasPerdidos.grid(row=0, column=0, sticky=NSEW)
            frameTablasPerdidos.grid_columnconfigure(0, weight=1)
            frameTablasPerdidos.grid_rowconfigure(0, weight=1)

            self.tablaSeguidoresPerdidos = Tableview(frameTablasPerdidos, coldata=['Usuario que dejaron de seguir al espiado'], rowdata=dejaronDeSeguirList, searchable=True, autofit=True)
            self.tablaSeguidoresPerdidos.align_column_center(cid=0)
            self.tablaSeguidoresPerdidos.align_heading_center(cid=0)
            self.tablaSeguidoresPerdidos.grid(row=0, column=0, sticky=NSEW)
            frameTablasPerdidos.grid_columnconfigure(0, weight=1)
            frameTablasPerdidos.grid_rowconfigure(0, weight=1)
            buttonVerSeguidorPerdido = tb.Button(frameTablasPerdidos, text='Ver usuario que dejó de seguir a espiado', command=self.Abrir_Ventana_Seguidor_Perdido)
            buttonVerSeguidorPerdido.grid(row=1, column=0)
            frameTablasPerdidos.grid_rowconfigure(1, weight=0)

            self.tablaSeguidosPerdidos = Tableview(frameTablasPerdidos, coldata=['Usuarios que el espiado dejó de seguir'], rowdata=dejoDeSeguirList, searchable=True, autofit=True)
            self.tablaSeguidosPerdidos.align_column_center(cid=0)
            self.tablaSeguidosPerdidos.align_heading_center(cid=0)
            self.tablaSeguidosPerdidos.grid(row=0, column=1, sticky=NSEW)
            frameTablasPerdidos.grid_columnconfigure(1, weight=1)
            buttonVerFolloweePerdido = tb.Button(frameTablasPerdidos, text='Ver usuario que el espiado dejó de seguir', command=self.Abrir_Ventana_Followee_Perdido)
            buttonVerFolloweePerdido.grid(row=1, column=1)
            frameTablasPerdidos.grid_columnconfigure(1, weight=0)

            self.imgCacheSeguidoresPerdidos = {}
            self.imgCacheFolloweesPerdidos = {}

            ventanaResultadosPerdidos.update_idletasks()
            ventanaResultadosPerdidos.deiconify()
            ventanaResultadosPerdidos.lift()

            #Se acomoda en una lista de listas para la tabla:
        except:
            messagebox.showerror(title='Error', message='No has seleccionado los archivos correspondientes')
        
    def Abrir_Ventana_Seguidor_Perdido(self):
        tableRows = self.tablaSeguidoresPerdidos.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.longevoHrefFollowers:
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
            
            if user in self.imgCacheSeguidoresPerdidos:
                img = self.imgCacheSeguidoresPerdidos[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheSeguidoresPerdidos[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheSeguidoresPerdidos[user] = None

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

    def Abrir_Ventana_Followee_Perdido(self):
        tableRows = self.tablaSeguidosPerdidos.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.longevoHrefFollowees:
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
            
            if user in self.imgCacheFolloweesPerdidos:
                img = self.imgCacheFolloweesPerdidos[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheFolloweesPerdidos[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheFolloweesPerdidos[user] = None

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


    def Comparar_Resultados_Ganados(self):
        try:
            longevoSeguidoresSet = set(self.longevoFollowers)
            longevoSeguidosSet = set(self.longevoFollowees)
            actualSeguidoresSet = set(self.actualFollowers)
            actualSeguidosSet = set(self.actualFollowees)

            # Seguidores nuevos (están en actual pero no en longevo)
            seguidoresNuevosSet = actualSeguidoresSet - longevoSeguidoresSet
            #Empezó a seguir:
            seguidosNuevosSet = actualSeguidosSet - longevoSeguidosSet

            #Se convierte en una lista para evitar no orden:
            seguidoresNuevosList = [[seguidorNuevo]for seguidorNuevo in seguidoresNuevosSet]
            seguidosNuevosList = [[seguidoNuevo]for seguidoNuevo in seguidosNuevosSet]

            #Se muestra la ventana con tablas e información
            ventanaResultadosGanados = tb.Toplevel()
            if os.name == 'nt':ventanaResultadosGanados.iconbitmap('img/StopStalking.ico')
            ventanaResultadosGanados.title('Ver usuarios que el espiado empezó a seguir y quién lo emepezó a seguir')
            ventanaResultadosGanados.withdraw()

            frameTablasGanadas = tb.Frame(ventanaResultadosGanados)
            frameTablasGanadas.grid(row=0, column=0, sticky=NSEW)
            frameTablasGanadas.grid_columnconfigure(0, weight=1)
            frameTablasGanadas.grid_rowconfigure(0, weight=1)

            self.tablaSeguidoresGanados = Tableview(frameTablasGanadas, coldata=['Usuario que empezó a seguir al espiado'], rowdata=seguidoresNuevosList, searchable=True, autofit=True)
            self.tablaSeguidoresGanados.align_column_center(cid=0)
            self.tablaSeguidoresGanados.align_heading_center(cid=0)
            self.tablaSeguidoresGanados.grid(row=0, column=0, sticky=NSEW)
            frameTablasGanadas.grid_columnconfigure(0, weight=1)
            frameTablasGanadas.grid_rowconfigure(0, weight=1)
            buttonVerSeguidorGanado = tb.Button(frameTablasGanadas, text='Ver usuario que empezó a seguir al espiado', command=self.Abrir_Ventana_Seguidor_Ganado)
            buttonVerSeguidorGanado.grid(row=1, column=0)
            frameTablasGanadas.grid_rowconfigure(1, weight=0)

            self.tablaSeguidosGanados = Tableview(frameTablasGanadas, coldata=['Usuarios que el espiado empezó a seguir'], rowdata=seguidosNuevosList, searchable=True, autofit=True)
            self.tablaSeguidosGanados.align_column_center(cid=0)
            self.tablaSeguidosGanados.align_heading_center(cid=0)
            self.tablaSeguidosGanados.grid(row=0, column=1, sticky=NSEW)
            frameTablasGanadas.grid_columnconfigure(1, weight=1)
            buttonVerFolloweeGanado = tb.Button(frameTablasGanadas, text='Ver usuario que el espiado empezó a seguir', command=self.Abrir_Ventana_Followee_Ganado)
            buttonVerFolloweeGanado.grid(row=1, column=1)
            frameTablasGanadas.grid_columnconfigure(1, weight=0)

            self.imgCacheSeguidoresGanados = {}
            self.imgCacheFolloweesGanados = {}

            ventanaResultadosGanados.update_idletasks()
            ventanaResultadosGanados.deiconify()
            ventanaResultadosGanados.lift()

        except:
            messagebox.showerror(title='Error', message='No has seleccionado los archivos correspondientes')

    def Abrir_Ventana_Seguidor_Ganado(self):
        tableRows = self.tablaSeguidoresGanados.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.actualHrefFollowers:
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
            
            if user in self.imgCacheSeguidoresGanados:
                img = self.imgCacheSeguidoresGanados[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheSeguidoresGanados[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheSeguidoresGanados[user] = None

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

    def Abrir_Ventana_Followee_Ganado(self):
        tableRows = self.tablaSeguidosGanados.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.actualHrefFollowees:
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
            
            if user in self.imgCacheFolloweesGanados:
                img = self.imgCacheFolloweesGanados[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheFolloweesGanados[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheFolloweesGanados[user] = None

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