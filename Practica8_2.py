import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

def process_frame():
    _, frame = cap.read()

    # Realizar balance de blancos en la imagen capturada
    frame_balanced = balance_de_blancos(frame)

    hsv = cv2.cvtColor(frame_balanced, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 90, 50])
    upper = np.array([60, 220, 180])

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame_balanced, frame_balanced, mask=mask)

    update_label(frame, label_frame)
    update_label(mask, label_mask)
    update_label(res, label_result)

    ventana.after(20, process_frame)

def balance_de_blancos(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg_gray = np.mean(img_gray)
    img_gray = img_gray * (255.0 / avg_gray)
    
    # Combinar la imagen original con la nueva versión ajustada en escala de grises
    balanced = np.zeros_like(img)
    for i in range(3):
        balanced[:,:,i] = np.clip(img[:,:,i] * (avg_gray / 255.0), 0, 255)
    
    return balanced

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

# Crear ventana
ventana = tk.Tk()
ventana.title("Procesamiento de Imágenes en Tiempo Real con Tkinter")

# Iniciar captura de la cámara
cap = cv2.VideoCapture(0)

# Crear etiquetas para mostrar las imágenes
label_frame = tk.Label(ventana)
label_frame.grid(row=0, column=0, padx=10, pady=10)

label_mask = tk.Label(ventana)
label_mask.grid(row=0, column=1, padx=10, pady=10)

label_result = tk.Label(ventana)
label_result.grid(row=0, column=2, padx=10, pady=10)

# Llamar a la función para procesar los fotogramas
process_frame()

# Mostrar la ventana
ventana.mainloop()

# Liberar la cámara
cap.release()