import requests
import io
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import webbrowser
import datetime

class Funcionalidades():

    @staticmethod
    def RequestImg(link):
        try:
            # Realizar la solicitud GET a la URL del perfil de Instagram
            response = requests.get(link, stream=True)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa

            image_data = io.BytesIO(response.content)
            
            # Abrir la imagen con PIL
            image = Image.open(image_data)
            
            return image

        except requests.exceptions.RequestException:
            Messagebox.show_error(title='Error al obtener foto', message='Hubo un error al tomar foto')
            return None
        
    @staticmethod
    def AbrirEnlace(event, url):
        webbrowser.open(url, new=2)

    @staticmethod
    def check_internet_connection():
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def ConvertirFecha(timestamp):
        # Convertir el timestamp a un objeto datetime en UTC
        dt_object_utc = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

        # Obtener la zona horaria local de la computadora
        zona_horaria_local = datetime.datetime.now().astimezone().tzinfo

        # Convertir el datetime de UTC a la zona horaria local
        dt_object_local = dt_object_utc.astimezone(zona_horaria_local)

        # Formatear la fecha y hora en una cadena legible
        return dt_object_local.strftime('%Y-%m-%d %H:%M:%S')