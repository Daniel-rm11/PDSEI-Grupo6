import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Función para aplicar el filtro pasa-bajos
def apply_filter(image, kernel_size):
    fil, col = image.shape

    img_padded = np.pad(image, ((0, fil), (0, col)), 'constant', constant_values=((0, 0), (0, 0)))

    f, c = np.ogrid[0:2*fil, 0:2*col]
    H = ((f - fil)**2 + (c - col)**2) <= (0.08 * fil * kernel_size)**2
    H_pb_ideal = np.int32(H)

    img_fft = np.fft.fft2(img_padded)
    img_fft_shift = np.fft.fftshift(img_fft)

    G_fft = img_fft_shift * H_pb_ideal

    G_fft_ishift = np.fft.ifftshift(G_fft)
    g = np.fft.ifft2(G_fft_ishift)
    g_real = np.real(g)[0:fil, 0:col]

    return g_real
# Función para escalar la imagen
def escalar_imagen(image, max_width):
    original_height, original_width = image.shape
    ratio = max_width / original_width
    height = int(original_height * ratio)
    return cv2.resize(image, (max_width, height))
# Función para mostrar la imagen en una etiqueta

def mostrar_imagen(image, label, max_width):
    imagen_resized = escalar_imagen(image, max_width)
    imagen_tk = ImageTk.PhotoImage(image=Image.fromarray(imagen_resized))
    label.config(image=imagen_tk)
    label.image = imagen_tk

# Función para mostrar el filtro en una etiqueta
def mostrar_filtro(kernel_size, label, fil, col):
    f, c = np.ogrid[0:fil, 0:col]
    D0 = 0.1 * fil
    D = np.sqrt((f - fil / 2)**2 + (c - col / 2)**2)
    H = np.exp(-(D**2) / (2 * (D0**2)))
    
    # Mostrar el filtro en una figura de matplotlib
    plt.figure(figsize=(8, 8))
    plt.imshow(H, cmap='gray')
    plt.axis('off')
    plt.savefig('filtro_frecuencial.png')  # Guardar el filtro como una imagen
    plt.close()

    # Cargar la imagen del filtro y mostrarla en la etiqueta
    filtro_img = cv2.imread('filtro_frecuencial.png', 0)
    imagen_tk = ImageTk.PhotoImage(image=Image.fromarray(filtro_img))
    label.config(image=imagen_tk)
    label.image = imagen_tk

# Función para actualizar el filtro y la imagen al mover el slider
def actualizar_filtro(valor):
    global img, label_imagen, label_filtro
    kernel_size = float(valor)
    img_filtered = apply_filter(img_original, kernel_size)
    mostrar_imagen(img_filtered, label_imagen, 300)
    mostrar_filtro(kernel_size, label_filtro, img.shape[0], img.shape[1])

# Cargar la imagen original
image_path = r"C:\ironman.jpg"
img_original = cv2.imread(image_path, 0)

# Crear la interfaz de usuario
ventana = tk.Tk()
ventana.title("Suavizado de Imagen con Filtro de Frecuencia")

label_imagen = tk.Label(ventana)
mostrar_imagen(img_original, label_imagen, 300)
label_imagen.grid(row=0, column=0, padx=10, pady=10)

label_filtro = tk.Label(ventana)
label_filtro.grid(row=0, column=1, padx=10, pady=10)

slider_n = tk.Scale(ventana, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                    label="Valor de n", command=actualizar_filtro)
slider_n.set(0.2)
slider_n.grid(row=1, column=0, columnspan=3, pady=10)

# Mostrar el filtro inicialmente con el valor predeterminado
mostrar_filtro(0.2, label_filtro, img_original.shape[0], img_original.shape[1])

ventana.mainloop()