import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

def segmentar_imagen():
    try:
        # Obtener los valores HSV ingresados por el usuario
        h_value = int(entry_h.get())
        s_value = int(entry_s.get())
        v_value = int(entry_v.get())

        # Definir el rango inferior y superior basado en los valores HSV ingresados
        lower = np.array([h_value - 10, max(0, s_value - 50), max(0, v_value - 50)])
        upper = np.array([h_value + 10, min(255, s_value + 50), min(255, v_value + 50)])

        # Convertir la imagen a espacio de color HSV
        hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        # Aplicar la segmentación utilizando el rango definido
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(original_image, original_image, mask=mask)

        # Actualizar la imagen segmentada en la interfaz
        update_label(result, label_result)

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores enteros para H, S, y V.")

def update_label(image, label):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = resize_image(image, 300)
    image = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image)
    label.config(image=image_tk)
    label.image = image_tk

def resize_image(image, max_width):
    original_height, original_width, _ = image.shape
    ratio = max_width / original_width
    height = int(original_height * ratio)
    return cv2.resize(image, (max_width, height))

def cargar_imagen():
    global original_image
    path = r"C:\Users\messi.jpg"  # Reemplazar con la ruta de tu imagen
    original_image = cv2.imread(path)
    update_label(original_image, label_original)

ventana = tk.Tk()
ventana.title("Segmentación por Espacio de Color")

# Crear etiquetas y entradas para valores HSV
label_h = tk.Label(ventana, text="Valor H:")
label_h.grid(row=0, column=0, padx=10, pady=10)
entry_h = tk.Entry(ventana)
entry_h.grid(row=0, column=1, padx=10, pady=10)

label_s = tk.Label(ventana, text="Valor S:")
label_s.grid(row=1, column=0, padx=10, pady=10)
entry_s = tk.Entry(ventana)
entry_s.grid(row=1, column=1, padx=10, pady=10)

label_v = tk.Label(ventana, text="Valor V:")
label_v.grid(row=2, column=0, padx=10, pady=10)
entry_v = tk.Entry(ventana)
entry_v.grid(row=2, column=1, padx=10, pady=10)

button_segmentar = tk.Button(ventana, text="Segmentar Imagen", command=segmentar_imagen)
button_segmentar.grid(row=3, columnspan=2, padx=10, pady=10)

# Etiqueta para mostrar la imagen original
label_original = tk.Label(ventana)
label_original.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

# Etiqueta para mostrar la imagen segmentada
label_result = tk.Label(ventana)
label_result.grid(row=0, column=3, rowspan=4, padx=10, pady=10)

# Botón para cargar una imagen
button_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
button_cargar.grid(row=4, columnspan=4, padx=10, pady=10)

ventana.mainloop()