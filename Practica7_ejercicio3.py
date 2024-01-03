import tkinter as tk
from PIL import Image, ImageTk
import numpy as np 
import cv2

def escalar_imagen(image, max_width):
    original_height,original_width = image.shape
    ratio = max_width / original_width
    height=int(original_height*ratio)
    return cv2.resize(image,(max_width,height))

def mostrar_imagen(image,label,max_width):
    imagen_resized=escalar_imagen(image,max_width)
    imagen_tk=ImageTk.PhotoImage(image=Image.fromarray(imagen_resized))
    label.config(image=imagen_tk)
    label.image=imagen_tk

def aplicar_filtro(image, filtro_size, A):
    fil, col = image.shape
    img_padded = np.pad(image, ((0, fil), (0, col)), 'constant', constant_values=((0, 0), (0, 0)))

    f, c = np.ogrid[0:2 * fil, 0:2 * col]
    D = np.sqrt((f - fil) ** 2 + (c - col) ** 2)

    # Filtro High Boost
    H_high_boost = 1 + A * (D - filtro_size) / filtro_size
    H_high_boost[D == 0] = 0

    img_fft = np.fft.fft2(img_padded)
    img_fft_shift = np.fft.fftshift(img_fft)

    G_fft = img_fft_shift * H_high_boost

    G_fft_ishift = np.fft.ifftshift(G_fft)
    g = np.fft.ifft2(G_fft_ishift)
    g_real = np.real(g)[0:fil, 0:col]

    # Normalizar y escalar al rango de uint8
    g_real_normalized = (g_real - np.min(g_real)) / (np.max(g_real) - np.min(g_real)) * 255
    g_real_uint8 = np.uint8(g_real_normalized)

    return g_real_uint8

def actualizar_filtro(filtro_size, A):
    global img

    # Convertir la imagen a int8
    img_int8 = np.uint8(img)

    # Aplicar filtro a la imagen y obtener la Transformada de Fourier
    imagen_filtrada = aplicar_filtro(img_int8, filtro_size, A)

    # Mostrar la imagen original
    mostrar_imagen(img, label_imagen, 300)

    # Mostrar el filtro frecuencial aplicado en escala de grises (0-255)
    fft_imagen = np.abs(np.fft.fftshift(np.fft.fft2(imagen_filtrada)))
    fft_imagen = np.log(fft_imagen + 1)  # Logaritmo para mejorar la visualización
    fft_imagen = 255 * fft_imagen / np.max(fft_imagen)

    mostrar_imagen(fft_imagen, label_matriz, 300)

    # Mostrar solo el resultado
    mostrar_imagen(imagen_filtrada, label_g_real, 300)

image_path=r"C:\Users\messi.jpg"
img=cv2.imread(image_path,0)

ventana = tk.Tk()
ventana.title("Mostrar Imagen y Filtro con Tkinter")

label_imagen = tk.Label(ventana)
mostrar_imagen(img, label_imagen, 300)
label_imagen.grid(row=0, column=0, padx=10, pady=10)

label_matriz = tk.Label(ventana)
label_matriz.grid(row=0, column=1, padx=10, pady=10)

label_g_real = tk.Label(ventana)
label_g_real.grid(row=0, column=2, padx=10, pady=10)

slider_n = tk.Scale(ventana, from_=1, to=20, orient=tk.HORIZONTAL,
                    label="Tamaño del filtro", command=lambda val: actualizar_filtro(int(val), slider_A.get()))
slider_n.set(2)
slider_n.grid(row=1, column=0, columnspan=3, pady=10)

slider_A = tk.Scale(ventana, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL,
                    label="Ganancia", command=lambda val: actualizar_filtro(slider_n.get(), float(val)))
slider_A.set(1)
slider_A.grid(row=2, column=0, columnspan=3, pady=10)

ventana.mainloop()