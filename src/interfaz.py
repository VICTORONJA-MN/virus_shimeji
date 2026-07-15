from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QMovie, QPainter, QTransform
import os
import sys
import random
from src.config import ANCHO_SPRITE, ALTO_SPRITE, VELOCIDAD, DISTANCIA_ALERTA

def obtener_ruta_recurso(carpeta, archivo):
    """ Resuelve la ruta tanto para desarrollo en VS Code como para el .exe compilado """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, carpeta, archivo)
    return os.path.join(carpeta, archivo)


class ContenedorGifEspejado(QLabel):
    """ Un QLabel modificado que intercepta el render del GIF y lo voltea físicamente """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.espejado = False

    def set_espejado(self, valor):
        if self.espejado != valor:
            self.espejado = valor
            self.update()

    def paintEvent(self, event):
        if not self.espejado:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        transformacion = QTransform()
        transformacion.translate(self.width(), 0)
        transformacion.scale(-1, 1)
        painter.setTransform(transformacion)

        movie = self.movie()
        if movie and movie.isValid():
            frame_actual = movie.currentPixmap()
            origen_x = (self.width() - frame_actual.width()) // 2
            origen_y = (self.height() - frame_actual.height()) // 2
            painter.drawPixmap(origen_x, origen_y, frame_actual)
        
        painter.end()


class ShimejiVentana(QWidget):
    def __init__(self):
        super().__init__()
        
        pantalla = QApplication.primaryScreen().geometry()
        self.ancho_pantalla = pantalla.width()
        self.alto_pantalla = pantalla.height()
        
        self.x_actual = float((self.ancho_pantalla - ANCHO_SPRITE) // 2)
        self.y_actual = float((self.alto_pantalla - ALTO_SPRITE) // 2)
        
        self.estado_actual = None 
        self.mirando_izquierda = True
        
        self.ocio_dx = 0.0
        self.ocio_dy = 0.0
        self.ticks_restantes_estado = 0
        
        self.init_ventana()
        self.init_animaciones()
        
        self.cambiar_animacion("ocio_quieto")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_logica)
        self.timer.start(30)

    def init_ventana(self):
        banderas = (
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        if sys.platform != "win32":
            banderas |= Qt.WindowType.SubWindow
            
        self.setWindowFlags(banderas)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.ancho_pantalla, self.alto_pantalla)

        self.contenedor_gif = ContenedorGifEspejado(self)
        self.contenedor_gif.setFixedSize(ANCHO_SPRITE, ALTO_SPRITE)
        self.contenedor_gif.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contenedor_gif.move(int(self.x_actual), int(self.y_actual))

        if sys.platform == "win32":
            import ctypes
            hwnd = int(self.winId())
            estilo_extendido = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, estilo_extendido | 0x20 | 0x80)
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)

    def init_animaciones(self):
        # Usamos obtener_ruta_recurso para que PyInstaller encuentre los archivos dentro del .exe temporal
        self.animaciones = {
            "ocio_quieto": QMovie(obtener_ruta_recurso("assets", "ocio_quieto.gif")),
            "ocio_caminar": QMovie(obtener_ruta_recurso("assets", "ocio_caminar.gif")),
            "ocio_dormir": QMovie(obtener_ruta_recurso("assets", "ocio_dormir.gif")),
            "emote1": QMovie(obtener_ruta_recurso("assets", "emote1.gif")),
            "emote2": QMovie(obtener_ruta_recurso("assets", "emote2.gif")),
            "emote3": QMovie(obtener_ruta_recurso("assets", "emote3.gif")),
            "emote4": QMovie(obtener_ruta_recurso("assets", "emote4.gif")),
            "emote5": QMovie(obtener_ruta_recurso("assets", "emote5.gif")),
            "huir_horizontal": QMovie(obtener_ruta_recurso("assets", "huir_horizontal.gif")),
            "huir_arriba": QMovie(obtener_ruta_recurso("assets", "huir_arriba.gif")),
            "huir_abajo": QMovie(obtener_ruta_recurso("assets", "huir_abajo.gif"))
        }
        
        tamano_objetivo = QSize(ANCHO_SPRITE, ALTO_SPRITE)
        for name, movie in self.animaciones.items():
            if movie.isValid():
                movie.setScaledSize(tamano_objetivo)
                movie.frameChanged.connect(self.contenedor_gif.update)

    def cambiar_animacion(self, nuevo_estado):
        if self.estado_actual == nuevo_estado:
            self.contenedor_gif.set_espejado(not self.mirando_izquierda)
            return 

        if self.estado_actual and self.animaciones[self.estado_actual].isValid():
            self.animaciones[self.estado_actual].stop()

        self.estado_actual = nuevo_estado
        movie = self.animaciones[nuevo_estado]

        if movie.isValid():
            self.contenedor_gif.setMovie(movie)
            movie.start()
        
        self.contenedor_gif.set_espejado(not self.mirando_izquierda)

    def tomar_decision_ocio(self):
        dados = random.randint(1, 100)

        if dados <= 40:
            self.cambiar_animacion("ocio_quieto")
            self.ocio_dx, self.ocio_dy = 0.0, 0.0
            self.ticks_restantes_estado = random.randint(100, 160)
        elif dados <= 75:
            self.cambiar_animacion("ocio_caminar")
            self.ocio_dx = random.choice([-1.5, 1.5])
            self.ocio_dy = random.choice([-0.5, 0.5])
            self.mirando_izquierda = True if self.ocio_dx < 0 else False
            self.ticks_restantes_estado = random.randint(200, 330)
        elif dados <= 85:
            self.cambiar_animacion("ocio_dormir")
            self.ocio_dx, self.ocio_dy = 0.0, 0.0
            self.ticks_restantes_estado = random.randint(260, 400)
        else:
            emote_elegido = f"emote{random.randint(1, 5)}"
            self.cambiar_animacion(emote_elegido)
            self.ocio_dx, self.ocio_dy = 0.0, 0.0
            self.ticks_restantes_estado = random.randint(100, 130)

    def actualizar_logica(self):
        pos_mouse = self.mapFromGlobal(QApplication.desktop().cursor().pos() if hasattr(QApplication, 'desktop') else self.cursor().pos())
        mouse_x = pos_mouse.x()
        mouse_y = pos_mouse.y()
        
        centro_x = self.x_actual + (ANCHO_SPRITE / 2.0)
        centro_y = self.y_actual + (ALTO_SPRITE / 2.0)

        dx = centro_x - mouse_x
        dy = centro_y - mouse_y
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia < DISTANCIA_ALERTA:
            if abs(dx) > abs(dy):
                self.cambiar_animacion("huir_horizontal")
                self.mirando_izquierda = False if dx > 0 else True
            else:
                if dy > 0:
                    self.cambiar_animacion("huir_arriba")
                else:
                    self.cambiar_animacion("huir_abajo")

            if dx != 0: self.x_actual += VELOCIDAD if dx > 0 else -VELOCIDAD
            if dy != 0: self.y_actual += VELOCIDAD if dy > 0 else -VELOCIDAD
            
            self.ticks_restantes_estado = 0
        else:
            if "huir" in str(self.estado_actual):
                self.cambiar_animacion("ocio_quieto")
                self.ticks_restantes_estado = 60 
                self.ocio_dx, self.ocio_dy = 0.0, 0.0

            self.ticks_restantes_estado -= 1
            if self.ticks_restantes_estado <= 0:
                self.tomar_decision_ocio()

            if self.estado_actual == "ocio_caminar":
                self.x_actual += self.ocio_dx
                self.y_actual += self.ocio_dy
                
                if self.x_actual <= 0 or self.x_actual >= self.ancho_pantalla - ANCHO_SPRITE:
                    self.ocio_dx *= -1
                    self.mirando_izquierda = not self.mirando_izquierda
                if self.y_actual <= 0 or self.y_actual >= self.alto_pantalla - ALTO_SPRITE:
                    self.ocio_dy *= -1

        self.x_actual = max(0, min(self.x_actual, self.ancho_pantalla - ANCHO_SPRITE))
        self.y_actual = max(0, min(self.y_actual, self.alto_pantalla - ALTO_SPRITE))

        self.contenedor_gif.move(int(self.x_actual), int(self.y_actual))
        self.contenedor_gif.set_espejado(not self.mirando_izquierda)