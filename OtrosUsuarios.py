import ttkbootstrap as tb
from ttkbootstrap.constants import *
import instaloader
import time
import os
from tkinter import filedialog, messagebox
from ttkbootstrap.dialogs import Messagebox
from SesionIniciada import ClaseSesionIniciada
from OtrosUsuariosJsonComparation import ClaseCompararJsonsOtrosUsers

class ClaseOtrosUsuarios():
    def __init__(self, mainWindow) -> None:
        self.OtrosUsuariosWindow = tb.Toplevel()
        if os.name == 'nt':self.OtrosUsuariosWindow.iconbitmap('img/StopStalking.ico')
        self.OtrosUsuariosWindow.title("Otros Usuarios")
        self.OtrosUsuariosWindow.withdraw()

        self.Widgets()

        self.mainWindow = mainWindow

        self.mainWindow.withdraw()  # Assuming mainWindow is the previous window to destroy
        self.OtrosUsuariosWindow.update_idletasks()
        self.OtrosUsuariosWindow.update()
        self.OtrosUsuariosWindow.deiconify()
        self.OtrosUsuariosWindow.lift()
        #Si esta ventana se destruye se llama a la función la cual destruye la ventana principal
        self.OtrosUsuariosWindow.protocol("WM_DELETE_WINDOW",lambda:self.Ventana_Destruida(mainWindow))
        self.OtrosUsuariosWindow.mainloop()

    def Ventana_Destruida(self, ventana):
            ventana.destroy()

    def Widgets(self):

        menuBar = tb.Menu(self.OtrosUsuariosWindow)

        menuVer = tb.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Ver', menu=menuVer)
        menuVer.add_command(label='Comparar JSONs entre fechas', command=ClaseCompararJsonsOtrosUsers)

        self.OtrosUsuariosWindow.config(menu=menuBar)

        fatherFrame = tb.Frame(self.OtrosUsuariosWindow)
        fatherFrame.grid(row=0, column=0, sticky=NSEW)
        self.OtrosUsuariosWindow.grid_columnconfigure(0, weight=1)
        self.OtrosUsuariosWindow.grid_rowconfigure(0, weight=1)

        labelUsuario = tb.Label(fatherFrame, text='Usuario')
        labelUsuario.grid(row=0, column=0)
        fatherFrame.grid_columnconfigure(0, weight=1)
        fatherFrame.grid_rowconfigure(0, weight=1)

        self.entryUsuario = tb.Entry(fatherFrame)
        self.entryUsuario.grid(row=1, column=0)
        fatherFrame.grid_rowconfigure(1, weight=1)

        labelContrasena = tb.Label(fatherFrame, text='Contraseña')
        labelContrasena.grid(row=2, column=0, pady=10)
        fatherFrame.grid_rowconfigure(2, weight=1)

        self.entryContrasena = tb.Entry(fatherFrame, show='*')
        self.entryContrasena.grid(row=3, column=0)
        fatherFrame.grid_rowconfigure(3, weight=1)

        buttonInciar = tb.Button(fatherFrame, text='INICIAR',command=self.Iniciar_Sesion)
        buttonInciar.grid(row=4, column=0, pady=25)
        fatherFrame.grid_rowconfigure(4, weight=1)

        buttonCargar = tb.Button(fatherFrame, text='CARGAR SESIÓN', command=self.Cargar_Sesion)
        buttonCargar.grid(row=5, column=0)
        fatherFrame.grid_rowconfigure(5, weight=1)

    def Iniciar_Sesion(self):
        user = self.entryUsuario.get()
        password = self.entryContrasena.get()

        L = instaloader.Instaloader()
        try:
            # Intentar iniciar sesión
            L.login(user, password)
            messagebox.showinfo(title="Inicio de Sesión Exitoso", message="Las credenciales son correctas. Ahora elige dónde guardar la sesión.")

            # Si las credenciales son correctas, preguntar dónde guardar la sesión
            file_path = filedialog.asksaveasfilename(
                title="Guardar sesión de Instagram"
            )

            if file_path:  # Si el usuario seleccionó un nombre de archivo y directorio
                # Guardar la sesión en el archivo seleccionado
                L.save_session_to_file(file_path)
                messagebox.showinfo(title="Sesión Guardada", message=f"Sesión guardada en: {file_path}")
                WindowSI = ClaseSesionIniciada(self.mainWindow, user, L)
            else:
                messagebox.showwarning(title="Guardar Sesión", message="No se seleccionó ningún archivo. La sesión no se guardó.")
                WindowSI = ClaseSesionIniciada(self.mainWindow, user, L)

        except instaloader.exceptions.BadCredentialsException:
            # Si las credenciales no son correctas
            messagebox.showerror(title="Error de Credenciales", message="Usuario o contraseña incorrectos. Inténtelo de nuevo.")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            messagebox.showerror(title='Error', message='La autenticación en dos factores está habilitada. Desactívala temporalmente e intenta nuevamente.')
        except instaloader.exceptions.ConnectionException:
            messagebox.showerror(title='Error', message='Problema de conexión. Verifica tu conexión a Internet e intenta nuevamente.')
        except:
            # Otros errores
            messagebox.showerror(title="Error", message="Ocurrió un error")

    def Cargar_Sesion(self):
        L = instaloader.Instaloader()
        try:
            # Abrir diálogo para seleccionar archivo de sesión
            file_path = filedialog.askopenfilename(
                title="Cargar sesión de Instagram"
            )

            if file_path:  # Si el usuario seleccionó un archivo
                if os.path.isfile(file_path):
                    try:
                        username = os.path.basename(file_path).split('-')[0]  # Extraer el nombre de usuario del archivo de sesión
                        L.load_session_from_file(username, file_path)
                        L.save_session_to_file(file_path)
                        messagebox.showinfo(title="Sesión Cargada", message=f"Sesión cargada desde: {file_path}")
                        WindowSI = ClaseSesionIniciada(self.mainWindow, username, L)
                    except Exception:
                        messagebox.showerror(title="Error", message="Ocurrió un error al cargar la sesión.\nEscoge el archivo correcto")
                else:
                    messagebox.showerror(title="Error", message="El archivo seleccionado no es válido o no existe.")
            else:
                messagebox.showwarning(title="Cargar Sesión", message="No se seleccionó ningún archivo. La sesión no se cargó.")
        
        except instaloader.exceptions.BadCredentialsException:
            # Si las credenciales no son correctas
            messagebox.showerror(title="Error de Credenciales", message="Usuario o contraseña incorrectos. Inténtelo de nuevo.")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            messagebox.showerror(title='Error', message='La autenticación en dos factores está habilitada. Desactívala temporalmente e intenta nuevamente.')
        except instaloader.exceptions.ConnectionException:
            messagebox.showerror(title='Error', message='Problema de conexión. Verifica tu conexión a Internet e intenta nuevamente.')
        except Exception as e:
            # Manejo de otros errores
            messagebox.showerror(title="Error", message="Ocurrió un error al cargar la sesión")
            print(type(e))
            print(e)
