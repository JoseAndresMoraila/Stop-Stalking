import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk
import json
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from urllib3.exceptions import MaxRetryError, NewConnectionError, NameResolutionError
import requests
import instaloader
from ayudaGui import ayudaClase
from compararFechas import ClaseVentanaCompararSeguidores
from Herramientas import Funcionalidades
from OtrosUsuarios import ClaseOtrosUsuarios
import os

class Principal():
    def __init__(self, root:tb.Window=None) -> None:
        root.withdraw()
        self.framePrincipal = tb.Frame(root)
        self.framePrincipal.grid(row=0, column=0, sticky='nsew')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.menuBar = tb.Menu(root)
        menuVer = tb.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Ver', menu=menuVer)
        menuVer.add_command(label='Comparar seguidores entre fechas', command=ClaseVentanaCompararSeguidores)

        menuAyuda = tb.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Ayuda', menu=menuAyuda)
        menuAyuda.add_command(label='JSON de Instagram', command=ayudaClase)

        menuOtros = tb.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Otros', menu=menuOtros)
        menuOtros.add_command(label='Otros usuarios', command=lambda: ClaseOtrosUsuarios(root))

        root.config(menu=self.menuBar)
        self.Widgets()
        root.update_idletasks()
        root.deiconify()
        root.lift()
        root.mainloop()

    def Widgets(self):
        stilo = tb.Style().configure('Anima.TButton', font=('Arial', 15), background='#1F2B75', bordercolor='#1F2B75', borderwidth=0)

        labelSeguidores = tb.Label(self.framePrincipal, text='Selecciona archivo de seguidores (Algo así como \"followers_1.json\")')
        labelSeguidores.grid(row=0, column=0, pady=15)
        self.framePrincipal.grid_columnconfigure(0, weight=1)
        self.framePrincipal.grid_rowconfigure(0, weight=1)

        buttonSeguidores = tb.Button(self.framePrincipal, text='Seleccionar followers_1.json', command=self.Elegir_Json_Followers)
        buttonSeguidores.grid(row=1, column=0)
        self.framePrincipal.grid_rowconfigure(1, weight=1)

        labelSeguidos = tb.Label(self.framePrincipal, text='Selecciona archivo de seguidos (Algo así como \"following.json\")')
        labelSeguidos.grid(row=2, column=0, pady=15)
        self.framePrincipal.grid_rowconfigure(2, weight=1)

        buttonSeguidores = tb.Button(self.framePrincipal, text='Seleccionar following.json', command=self.Elegir_Json_Following)
        buttonSeguidores.grid(row=3, column=0, pady=15)
        self.framePrincipal.grid_rowconfigure(3, weight=1)

        buttonVer = tb.Button(self.framePrincipal, text='Ver Personas Que Sigues Pero No Te Siguen', command=self.Ver_Tabla_No_Te_Siguen, style="Anima.TButton")
        buttonVer.grid(row=4, column=0)
        self.framePrincipal.grid_rowconfigure(4, weight=1)

        buttonVer = tb.Button(self.framePrincipal, text='Ver Personas Que Te Siguen pero No Sigues', command=self.Ver_Tabla_No_Los_Sigues, style="Anima.TButton")
        buttonVer.grid(row=5, column=0, pady=10)
        self.framePrincipal.grid_rowconfigure(5, weight=1)

    def Elegir_Json_Followers(self):
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo seguidores',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.dataFollowers = json.load(file)

                values = []
                hrefFollowers= []
                self.followersTimestampDic = {}

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for entry in self.dataFollowers:
                        for string_data in entry["string_list_data"]:
                            # Extraer el valor de "value" y añadirlo 
                            values.append(string_data["value"])
                            hrefFollowers.append(string_data["href"])
                            ususario = string_data["value"]
                            tiempo = string_data["timestamp"]
                            self.followersTimestampDic[ususario] = tiempo

                    self.followersTuple = tuple(values)
                    self.followersHrefTuple = tuple(hrefFollowers)
                except: Messagebox.show_error("Archivo incorrecto", "Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")

            except json.JSONDecodeError:
                Messagebox.show_error(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser algo como \"followers_1.json\"")

    def Elegir_Json_Following(self):
        followersJSONfile = filedialog.askopenfilename(title='Seleccionar archivo seguidos',
        filetypes=[("JSON", "*.json"),("Todos los archivos", "*.*")])
        if followersJSONfile:
            try:
                with open(followersJSONfile, 'r') as file:
                    self.dataFollowing = json.load(file)

                values = []
                hrefFollowing= []
                self.followingTimestampDic = {}

                # Iterar sobre cada elemento en "relationships_following"
                try:
                    for relationship in self.dataFollowing["relationships_following"]:
                        # Iterar sobre cada elemento en "string_list_data"
                        for string_data in relationship["string_list_data"]:
                            # Extraer el valor de "value" y añadirlo a la lista
                            values.append(string_data["value"])
                            hrefFollowing.append(string_data["href"])
                            ususario = string_data["value"]
                            tiempo = string_data["timestamp"]
                            self.followingTimestampDic[ususario] = tiempo

                    self.followingTuple = tuple(values)
                    self.followingHrefTuple = tuple(hrefFollowing)
                except: Messagebox.show_error(title="Archivo incorrecto", message="Selecciona el acrhivo correcto, deber ser algo como \"following.json\"")
                
            except json.JSONDecodeError:
                Messagebox.show_error(title="Archivo no compatible", message="Selecciona el acrhivo correcto, deber ser algo como \"following.json\"")

    def Ver_Tabla_No_Te_Siguen(self):
        values = []
        try:
            for seguido in self.followingTuple:
                if seguido not in self.followersTuple:
                    timestamp = self.followingTimestampDic.get(seguido, None)
                    fechaLegible = Funcionalidades.ConvertirFecha(timestamp) if timestamp else 'Desconocido'
                    values.append((seguido, fechaLegible))

            noTeSiguenVentana = tb.Toplevel()
            if os.name == 'nt':noTeSiguenVentana.iconbitmap('img/StopStalking.ico')
            noTeSiguenVentana.title('Personas que sigues pero no te siguen')
            noTeSiguenVentana.withdraw()
            self.imgCacheNoTeSigue = {} #SE hace para en vez de cargar una petición cada vez que se entre se guarde la imagen en el caché
            frameNoTeSiguenVentana = tb.Frame(noTeSiguenVentana)
            frameNoTeSiguenVentana.grid(row=0, column=0, sticky=NSEW)
            noTeSiguenVentana.grid_rowconfigure(0, weight=1)
            noTeSiguenVentana.grid_columnconfigure(0, weight=1)

            self.tablaNoTeSiguen = Tableview(frameNoTeSiguenVentana, coldata=['Usuario', 'Fecha desde que los sigues'], rowdata=values, searchable=True, autofit=True)
            self.tablaNoTeSiguen.align_column_center(cid=0)
            self.tablaNoTeSiguen.align_heading_center(cid=0)
            self.tablaNoTeSiguen.align_column_center(cid=1)
            self.tablaNoTeSiguen.align_heading_center(cid=1)

            self.tablaNoTeSiguen.grid(row=0, column=0, sticky=NSEW)
            frameNoTeSiguenVentana.grid_rowconfigure(0, weight=1)
            frameNoTeSiguenVentana.grid_columnconfigure(0, weight=1)

            buttonSeeUser = tb.Button(frameNoTeSiguenVentana, text='VER USUARIO', command=self.Abrir_Ventana_Usuario_No_Te_Sigue)
            buttonSeeUser.grid(row=1, column=0, sticky=NSEW)
            frameNoTeSiguenVentana.grid_rowconfigure(1, weight=1)

            noTeSiguenVentana.update_idletasks()
            noTeSiguenVentana.deiconify()
            noTeSiguenVentana.lift()
        except Exception: Messagebox.show_error(title="Error", message="No has seleccionado los archivos correctamente")

    def Ver_Tabla_No_Los_Sigues(self):
        values = []
        try:
            for seguidor in self.followersTuple:
                if seguidor not in self.followingTuple:
                    timestamp = self.followersTimestampDic.get(seguidor, None)
                    fechaLegible = Funcionalidades.ConvertirFecha(timestamp) if timestamp else 'Desconocido'
                    values.append((seguidor, fechaLegible))

            noSiguesVentana = tb.Toplevel()
            if os.name == 'nt':noSiguesVentana.iconbitmap('img/StopStalking.ico')
            noSiguesVentana.title('Personas que te siguen pero no sigues')
            noSiguesVentana.withdraw()
            self.imgCacheNoLoSigues = {} #SE hace para en vez de cargar una petición cada vez que se entre se guarde la imagen en el caché
            frameNoSiguesVentana = tb.Frame(noSiguesVentana)
            frameNoSiguesVentana.grid(row=0, column=0, sticky=NSEW)
            noSiguesVentana.grid_rowconfigure(0, weight=1)
            noSiguesVentana.grid_columnconfigure(0, weight=1)

            self.tablaNoLosSigues = Tableview(frameNoSiguesVentana, coldata=['Usuario', 'Fecha desde que te sigue'], rowdata=values, searchable=True, autofit=True)
            self.tablaNoLosSigues.align_column_center(cid=0)
            self.tablaNoLosSigues.align_heading_center(cid=0)
            self.tablaNoLosSigues.align_column_center(cid=1)
            self.tablaNoLosSigues.align_heading_center(cid=1)

            self.tablaNoLosSigues.grid(row=0, column=0, sticky=NSEW)
            frameNoSiguesVentana.grid_rowconfigure(0, weight=1)
            frameNoSiguesVentana.grid_columnconfigure(0, weight=1)

            buttonSeeUser = tb.Button(frameNoSiguesVentana, text='VER USUARIO', command=self.Abrir_Ventana_Usuario_No_Lo_Sigues)
            buttonSeeUser.grid(row=1, column=0, sticky=NSEW)
            frameNoSiguesVentana.grid_rowconfigure(1, weight=1)

            noSiguesVentana.update_idletasks()
            noSiguesVentana.deiconify()
            noSiguesVentana.lift()
        except: Messagebox.show_error(title="Error", message="No has seleccionado los archivos correctamente")

    def Abrir_Ventana_Usuario_No_Te_Sigue(self):
        tableRows = self.tablaNoTeSiguen.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.followingHrefTuple:
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
                windowVer.destroy()
                return
            
            if user in self.imgCacheNoTeSigue:
                img = self.imgCacheNoTeSigue[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheNoTeSigue[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheNoTeSigue[user] = None

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
            Messagebox.show_error(title='Error', message='Error desconocido')
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


    def Abrir_Ventana_Usuario_No_Lo_Sigues(self):
        tableRows = self.tablaNoLosSigues.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.followersHrefTuple:
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
            
            if user in self.imgCacheNoLoSigues:
                img = self.imgCacheNoLoSigues[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imgCacheNoLoSigues[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imgCacheNoLoSigues[user] = None

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