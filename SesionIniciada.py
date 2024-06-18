import ttkbootstrap as tb
from ttkbootstrap.constants import *
import instaloader
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError, NameResolutionError
from ttkbootstrap.dialogs import Messagebox
import json
from ttkbootstrap.tableview import Tableview
from Herramientas import Funcionalidades
from datetime import datetime
import os

class ClaseSesionIniciada():
    def __init__(self, mainWindow: tb.Window, user: str, Sesion: instaloader) -> None:
        self.WindowSesionIniciada = tb.Toplevel()
        if os.name == 'nt':self.WindowSesionIniciada.iconbitmap('img/StopStalking.ico')
        self.WindowSesionIniciada.title(user)

        self.Sesion = Sesion
        self.Widgets()

        self.WindowSesionIniciada.update_idletasks()
        self.WindowSesionIniciada.deiconify()
        self.WindowSesionIniciada.lift()
        self.WindowSesionIniciada.protocol("WM_DELETE_WINDOW", lambda: self.Ventana_Destruida(mainWindow))

    def Ventana_Destruida(self, ventanaMain: tb.Window):
        ventanaMain.destroy()

    def Widgets(self):
        fatherFrame = tb.Frame(self.WindowSesionIniciada)
        fatherFrame.grid(row=0, column=0, sticky=NSEW)
        self.WindowSesionIniciada.grid_columnconfigure(0, weight=1)
        self.WindowSesionIniciada.grid_rowconfigure(0, weight=1)

        labelUserToFind = tb.Label(fatherFrame, text='Usuario que deseas comparar quienes los siguen y si este los sigue de vuelta y viceversa')
        labelUserToFind.grid(row=0, column=0)
        fatherFrame.grid_columnconfigure(0, weight=1)
        fatherFrame.grid_rowconfigure(0, weight=1)

        self.entryUserToFind = tb.Entry(fatherFrame, width=30)
        self.entryUserToFind.grid(row=1, column=0)
        fatherFrame.grid_rowconfigure(1, weight=1)

        buttonComparar = tb.Button(fatherFrame, text='Comparar', command=self.Ver_Usuario)
        buttonComparar.grid(row=2, column=0)
        fatherFrame.grid_rowconfigure(2, weight=1)

        explicacionStr = 'El obtener la información puede tardar dependiendo la cantidad de seguidores y seguidos del usaurio a espiar.\nO puede arrojar el error 401 el cual si guardaste la sesión tienes que borrarlo y volver a inicar sesión,\npero recuerda no abusar de esto porque Instagram te pedirá volver a inicar sesión en tu celular.'
        labelEXplicacion = tb.Label(fatherFrame, text=labelEXplicacion)
        labelEXplicacion.grid(row=3, column=0, pady=20)
        fatherFrame.grid_rowconfigure(3, weight=1)

    def Ver_Usuario(self):
        usernameVer = self.entryUserToFind.get()
        if usernameVer:
            try:
                
                # Usa la función cacheada para obtener los seguidores y seguidos
                self.listaSeguidos, self.listaSeguidores = self.Obtener_Perfil(usernameVer)

                self.enlacesSeguidos = [f"https://www.instagram.com/{username}/" for username in self.listaSeguidos]
                self.enlacesSeguidores = [f"https://www.instagram.com/{username}/" for username in self.listaSeguidores]

                self.listNoEsSeguidoPor = []
                for seguido in self.listaSeguidos:
                    if seguido not in self.listaSeguidores:
                        self.listNoEsSeguidoPor.append([seguido])

                self.listNoSigueA = []
                for seguidor in self.listaSeguidores:
                    if seguidor not in self.listaSeguidos:
                        self.listNoSigueA.append([seguidor])

                self.Ver_Diferencias(usernameVer)

            except instaloader.exceptions.ProfileNotExistsException:
                messagebox.showerror(title='Usuario no existe', message=f'El usuario {usernameVer} no existe')
            except Exception as e:
                messagebox.showerror(title='Error', message='Hubo algún error al recuperar información de perfil. Checa si en tu celular se cerró sesión y vuleve a inicarla.\nO en vez de cargar desde el archivo la sesión vuleve a inicar sesión: ' + str(e) + '\n\nSi te sale error 401 checa tu teléfono y vuelve a inicar sesión en el y en este programa también y checa en seguridad donde iniciaste sesión.')


    def Ver_Diferencias(self, user:str):
        windowTablasDiferencias = tb.Toplevel()
        if os.name == 'nt':windowTablasDiferencias.iconbitmap('img/StopStalking.ico')
        windowTablasDiferencias.withdraw()
        windowTablasDiferencias.title("Ver diferencias")

        framePrincipal = tb.Frame(windowTablasDiferencias)
        framePrincipal.grid(row=0, column=0, sticky=NSEW)
        windowTablasDiferencias.grid_rowconfigure(0, weight=1)
        windowTablasDiferencias.grid_columnconfigure(0, weight=1)

        self.tablaNoEsSeguidoPor = Tableview(framePrincipal, coldata=[f'Usuarios que {user} sigue pero no le siguen de vuelta'], rowdata=self.listNoEsSeguidoPor, searchable=True, autofit=True)
        self.tablaNoEsSeguidoPor.align_column_center(cid=0)
        self.tablaNoEsSeguidoPor.align_heading_center(cid=0)
        self.tablaNoEsSeguidoPor.grid(row=0, column=0, sticky=NSEW)
        framePrincipal.grid_columnconfigure(0, weight=1)
        framePrincipal.grid_rowconfigure(0, weight=1)

        self.tablaNoSigueA = Tableview(framePrincipal, coldata=[f'Usuarios que siguen a {user} pero este no los sigue de vuelta'], rowdata=self.listNoSigueA, searchable=True, autofit=True)
        self.tablaNoSigueA.align_column_center(cid=0)
        self.tablaNoSigueA.align_heading_center(cid=0)
        self.tablaNoSigueA.grid(row=0, column=1, sticky=NSEW)
        framePrincipal.grid_columnconfigure(0, weight=1)

        buttonVerUsuarioNoSeguido = tb.Button(framePrincipal, text=f'Ver usuario que {user} sigue pero no es seguido de vuelta', command=self.Abrir_Ventana_Usuario_No_Sigue_A_Espiado)
        buttonVerUsuarioNoSeguido.grid(column=0, row=1)
        framePrincipal.grid_rowconfigure(1, weight=1)

        buttonVerUsuarioNoSgueA = tb.Button(framePrincipal, text=f'Ver usuario que sigue a {user} pero este no lo sigue de vuelta', command=self.Abrir_Ventana_Espiado_No_Sigue_A_User)
        buttonVerUsuarioNoSgueA.grid(row=1, column=1)
        framePrincipal.grid_columnconfigure(1, weight=1)

        stilo = tb.Style()
        stilo.configure('SaveEspiado.TButton', background='#2043DF', bordercolor='2043DF', borderwidth=0)
        stilo.map('SaveEspiado.TButton',background=[("active", "#193098")]) #Esto hace que al apsar el mouse por arriba cambie de color

        buttonGuardarJsonFolloweesFollowers = tb.Button(framePrincipal, command=self.Guardar_Info_Espiado_Json, style="SaveEspiado.TButton", text='Guardar JSON de seguidores y seguidos de usuario espiado\n(Este JSON sirve para hacer comparaciones de seguidores y seguidos del usuario espaid\nentre fechas para saber si dejó de seguir o alguien lo siguió y viceversa)')
        buttonGuardarJsonFolloweesFollowers.grid(row=2, column=0, sticky=NSEW, columnspan=2, pady=10)
        framePrincipal.grid_rowconfigure(2, weight=1)

        self.imagenesCacheUserNoSigueAespiado = {}
        self.imagenesCacheEspiadoNoSigueAuser = {}

        windowTablasDiferencias.update_idletasks()
        windowTablasDiferencias.deiconify()
        windowTablasDiferencias.lift()

    def Abrir_Ventana_Usuario_No_Sigue_A_Espiado(self):
        tableRows = self.tablaNoEsSeguidoPor.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.enlacesSeguidos:
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
            
            if user in self.imagenesCacheUserNoSigueAespiado:
                img = self.imagenesCacheUserNoSigueAespiado[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imagenesCacheUserNoSigueAespiado[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imagenesCacheUserNoSigueAespiado[user] = None

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

    def Abrir_Ventana_Espiado_No_Sigue_A_User(self):
        tableRows = self.tablaNoSigueA.get_rows(selected=True)
        for row in tableRows:
            user = row.values[0]
        
        # Find the correct href for the user
        enlace = None
        for href in self.enlacesSeguidores:
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
            
            if user in self.imagenesCacheEspiadoNoSigueAuser:
                img = self.imagenesCacheEspiadoNoSigueAuser[user]
            else:
                bot = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(bot.context, user)
                img = Funcionalidades.RequestImg(profile.profile_pic_url)
                if img:
                    img = img.resize((500, 500), Image.LANCZOS)
                    self.imagenesCacheEspiadoNoSigueAuser[user] = img
                    self.img_tk = ImageTk.PhotoImage(img)
                else:
                    self.imagenesCacheEspiadoNoSigueAuser[user] = None

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

    def Obtener_Perfil(self, username):
        profile = instaloader.Profile.from_username(self.Sesion.context, username)
        
        listaSeguidos = [followee.username for followee in profile.get_followees()]
        listaSeguidores = [follower.username for follower in profile.get_followers()]

        return listaSeguidos, listaSeguidores
    
    def Guardar_Info_Espiado_Json(self):
        toJsonFollowers = [{"username": follower, "link": f"https://www.instagram.com/{follower}/"} for follower in self.listaSeguidores]
        toJsonFollowing = [{"username": followee, "link": f"https://www.instagram.com/{followee}/"}for followee in self.listaSeguidos]
        data = {"followers": toJsonFollowers, "followees": toJsonFollowing}

        fecha_actual_str = datetime.now().strftime("%d-%m-%Y")
        espiado = self.entryUserToFind.get()
        initialNameFile = f'{espiado} {fecha_actual_str} info.json'

        file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
        title=f"Guardar seguidores y seguidos de {espiado} en JSON",
        initialfile=initialNameFile)

        if file_path:
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                messagebox.showinfo(title="Éxito", message=f'Datos guardados en {file_path}')
            except:
                messagebox.showerror(title='Error', message='Hubo un error al guardar el archivo')
        else:
            messagebox.showwarning(title='Guardado cancelado', message='Se canceló el guardado de archivo')

    