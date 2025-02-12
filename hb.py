import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
from PIL import Image
import os
import numpy as np
import sys

# Determinar si el script está corriendo como un archivo empaquetado (con PyInstaller)
if getattr(sys, 'frozen', False):
    # Si es un archivo empaquetado, obtener la ruta desde el ejecutable
    bundle_dir = sys._MEIPASS
else:
    # Si es un script normal, obtener la ruta del directorio actual
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta de los archivos
image_path = os.path.join(bundle_dir, 'img.png')
music_path = os.path.join(bundle_dir, 'Moments.mp3')

# Configuración de pygame para la música
def play_music(music_file):
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Reproducción en bucle

# Crear la figura y cargar la imagen
fig, ax = plt.subplots()
fig.set_facecolor("black")

# Cargar la imagen
img = Image.open(image_path)

# Mostrar la imagen en el centro
imagebox = ax.imshow(img, extent=[-1, 1, -1, 1], zorder=2)  # Establecer zorder mayor para la imagen

# Quitar ejes
ax.axis("off")

# Arte ASCII para "Feliz cumpleaños"
ascii_art = """
▄  █ ██   █ ▄▄  █ ▄▄ ▀▄    ▄     ███   ▄█ █▄▄▄▄    ▄▄▄▄▀ ▄  █ ██▄   ██  ▀▄    ▄
█   █ █ █  █   █ █   █  █  █      █  █  ██ █  ▄▀ ▀▀▀ █   █   █ █  █  █ █   █  █
██▀▀█ █▄▄█ █▀▀▀  █▀▀▀    ▀█       █ ▀ ▄ ██ █▀▀▌      █   ██▀▀█ █   █ █▄▄█   ▀█
█   █ █  █ █     █       █        █  ▄▀ ▐█ █  █     █    █   █ █  █  █  █   █
   █     █  █     █    ▄▀         ███    ▐   █     ▀        █  ███▀     █ ▄▀
  ▀     █    ▀     ▀                        ▀              ▀           █
       ▀                                                              ▀
"""

# Añadir el arte ASCII en la parte superior (color blanco fijo)
ascii_text = ax.text(0, 1.5, ascii_art, color="white", fontsize=6, ha="center", va="center", family="monospace", zorder=3)


text_name = ax.text(0, -1.5, """
   ▄   ██   █▀▄▀█ ▄███▄   
    █  █ █  █ █ █ █▀   ▀  
██   █ █▄▄█ █ ▄ █ ██▄▄    
█ █  █ █  █ █   █ █▄   ▄▀ 
█  █ █    █    █  ▀███▀   
█   ██   █    ▀           
        ▀                 
""", color="white", fontsize=6, ha="center", va="center", weight="bold", family="monospace", zorder=3)

# Crear texto adicional alrededor de la imagen (fuera de la imagen)
extra_texts = [
    ("¡Feliz día!", 1, 0.8),  # Fuera de la imagen, encima a la derecha
    ("¡descansa en paz gaaa!", -1, 0.8),  # Fuera de la imagen, encima a la izquierda
    ("¡Con mucho cariño!", 1, -0.8),  # Fuera de la imagen, debajo a la derecha
    ("eri gei?", -1, -0.8)  # Fuera de la imagen, debajo a la izquierda
]

# Añadir los textos extra a la figura
extra_text_objects = []
for text, x, y in extra_texts:
    extra_text = ax.text(x, y, text, color="white", fontsize=6, ha="center", va="center", family="monospace", zorder=3)
    extra_text.set_alpha(0)  # Comenzamos con opacidad 0, es decir, invisible
    extra_text_objects.append(extra_text)

# Crear estrellas pequeñas aleatorias en el fondo
num_stars = 80  # Número de estrellas
star_x = np.random.uniform(-1, 1, num_stars)
star_y = np.random.uniform(-1, 1, num_stars)
star_sizes = np.random.uniform(1, 5, num_stars)  # Tamaño de las estrellas
star_opacity = np.zeros(num_stars)  # Comienzan invisibles

# Estrellas como puntos (zorder 1 para que estén al fondo)
stars = ax.scatter(star_x, star_y, s=star_sizes, color="#FFC300", alpha=0, zorder=1)

# Función de actualización de la animación
def update(frame):
    global star_opacity  # Usamos la variable global para modificarla dentro de la función
    
    # Animar el texto "JOHAKIN" con pulso (sin cambio de color)
    scale_factor_text = 1 + 0.1 * np.sin(frame / 5.0)  # Efecto de pulso para el texto
    text_name.set_fontsize(6 * scale_factor_text)  # Cambiar el tamaño de la fuente
    
    # El texto ASCII de arriba (se mantiene blanco y sin cambio de color)
    ascii_text.set_fontsize(6 * (1 + 0.1 * np.sin(frame / 5.0)))  # Animar el tamaño del texto ASCII

    # Animar la imagen con pulso
    scale_factor_image = 1 + 0.05 * np.sin(frame / 5.0)  # Efecto de pulso para la imagen
    imagebox.set_extent([-1 * scale_factor_image, 1 * scale_factor_image, 
                         -1 * scale_factor_image, 1 * scale_factor_image])  # Cambiar el tamaño de la imagen

    # Animar las estrellas para que aparezcan lentamente
    star_opacity += 0.01  # Incrementar la opacidad gradualmente
    star_opacity = np.clip(star_opacity, 0, 1)  # Limitar la opacidad entre 0 y 1
    stars.set_alpha(star_opacity)  # Aplicar opacidad a las estrellas

   # Animar los textos adicionales para que aparezcan lentamente, uno por uno
    for i, extra_text in enumerate(extra_text_objects):
        if frame > (i * 20):  # Hacer que aparezca después de cierto número de frames
         extra_text.set_alpha(min(0.05 * (frame - i * 20), 1))  # Limitar la opacidad entre 0 y 1

    return [ascii_text, imagebox, text_name, stars] + extra_text_objects

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=100, interval=50, repeat=True)

# Ajustar el tamaño de la ventana para que se vea bien todo
fig.tight_layout(pad=2.0)
plt.gcf().set_size_inches(8, 6)  # Ajusta el tamaño según tus necesidades

# Función para centrar la ventana
def center_window():
    window = plt.gcf().canvas.manager.window  # Obtener la ventana de matplotlib
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int((screen_height - height) / 2)
    position_left = int((screen_width - width) / 2)
    window.geometry(f'{width}x{height}+{position_left}+{position_top}')

# Reproducir música de fondo
if os.path.exists(music_path):
    play_music(music_path)
else:
    print("No se encontró el archivo de música. Por favor, asegúrate de tener un archivo llamado 'Moments.mp3' en la misma carpeta.")

# Llamar a la función para centrar la ventana después de mostrarla
plt.show()
center_window()

# Detener música al cerrar
pygame.mixer.quit()
