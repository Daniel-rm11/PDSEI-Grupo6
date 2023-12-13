
# coding: utf-8

# In[39]:

import cv2
slider_max = 100
title_window = 'Brillo'



def on_trackbar(val):
    dst = src1 + val/255
    cv2.imshow(title_window, dst)

src1 = cv2.imread(r"C:\ironman.jpg") / 255


try:
    cv2.namedWindow(title_window)
    trackbar_name = f"Brilo {slider_max}"
    cv2.createTrackbar(trackbar_name, title_window, 0, slider_max, on_trackbar)
    on_trackbar(0)

    while True:
        key = cv2.waitKey(1)
        if key != -1:
             break
    cv2.destroyAllWindows()
except:
    cv2.destroyAllWindows()


# In[4]:


import cv2
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


slider_max = 100
title_window = 'Actividad 2: Suavizado'

def on_trackbar(val):
    brightness = val / slider_max
    img = cv2.imread(r"C:\ironman.jpg", 0) / 255
    img_with_brightness = np.clip(img + brightness, 0, 1)

    kernel = np.ones((11, 11)) / 121
    out = signal.convolve2d(img_with_brightness, kernel, mode="same")

    plt.figure(figsize=(15, 15))
    plt.subplot(121)
    plt.imshow(img_with_brightness, cmap="gray")
    plt.title("Imagen en gris")

    plt.subplot(122)
    plt.imshow(np.abs(out), cmap="gray", vmin=0, vmax=1)
    plt.title("Resultado de suavisado")
    plt.show()

src1 = cv2.imread(r"C:\ironman.jpg") / 255

try:
    cv2.namedWindow(title_window)
    trackbar_name = f"Brillo {slider_max}"
    cv2.createTrackbar(trackbar_name, title_window, 0, slider_max, on_trackbar)
    on_trackbar(0)

    while True:
        key = cv2.waitKey(1)
        if key != -1:
             break
    cv2.destroyAllWindows()
except:
    cv2.destroyAllWindows()


# In[40]:


import cv2
import numpy as np
from scipy import signal


slider_max = 10  # Ahora el slider irá del 0 al 10 en incrementos de 2
title_window = 'Actividad 2: Suavizado'

def on_trackbar(val):
    img = cv2.imread(r"C:\ironman.jpg", 0) / 255

    # Ajustar el tamaño del kernel según el valor del slicer (limitado al rango 1-20, incrementos de 2)
    kernel_size = 2 * val + 1
    kernel_size = np.clip(kernel_size, 1, 20)
    
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
    
    out = signal.convolve2d(img, kernel, mode="same")

    # Mostrar las imágenes en la misma ventana
    cv2.imshow(title_window, np.hstack([img, np.abs(out)]))

src1 = cv2.imread(r"C:\ironman.jpg") / 255

try:
    cv2.namedWindow(title_window)
    trackbar_name = f"Tamaño del Kernel (pares) {slider_max}"
    cv2.createTrackbar(trackbar_name, title_window, 0, slider_max, on_trackbar)
    on_trackbar(0)

    while True:
        key = cv2.waitKey(1)
        if key != -1:
             break
except:
    pass
finally:
    cv2.destroyAllWindows()


# In[ ]:


import cv2
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


slider_max_A = 5
title_window = 'Actividad 2: Filtro Laplaciano'

def on_trackbar_A(val):
    A = val / slider_max_A
    img = cv2.imread(r"C:\ironman.jpg", 0) / 255

    # Filtro Laplaciano
    kernel = np.array([[-1, -1, -1], [-1, A + 8, -1], [-1, -1, -1]])
    laplacian_out = signal.convolve2d(img, kernel, mode="same")

    # Mostrar las imágenes en la misma ventana
    cv2.imshow(title_window, np.hstack([img, laplacian_out]))

src1 = cv2.imread(r"C:\ironman.jpg") / 255

try:
    cv2.namedWindow(title_window)
    trackbar_name_A = f"A {slider_max_A}"
    cv2.createTrackbar(trackbar_name_A, title_window, 0, slider_max_A, on_trackbar_A)
    on_trackbar_A(0)

    while True:
        key = cv2.waitKey(1)
        if key != -1:
            break
except:
    pass
finally:
    cv2.destroyAllWindows()