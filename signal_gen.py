import time
import random

# Simulando señales EMG
def generate_emg_signal():
    
    # Ruido blanco con media gaussiana (0.5V y varianza de 0.05V)
    s_base = random.uniform(0.5, 0.05)
    
    # Contraccion por probabilidad
    if random.random() > 0.1: # Crea una float de 0.0 a 0.999 -> calculamos probabilidad
        spike = random.uniform(1.5, 2.5) # pico aleatorio de 1.2V a 2.5V -> mi rango normal debilucho
        return spike
    else:
        return s_base
    
window_size = 5 # definimos el tamaño de la ventana
buffer = [0.0] * window_size # creamos un array con ceros del tamaño de la ventana
index = 0 # creamos la variable que regula el index

# creando un umbral de detección:
threshold = 0.8

def sliding_filter(new_value):
    """
        Func que recibirá un nuevo valor cada 10ms y:
            - Lo guardará en el buffer
            - Actualiza el índice
            - Calcula el promedio
            - Devuelve el resultado

    """
    global index # tomamos una variable global y la modificamos acá
    buffer[index] = new_value # asignamos el valor
    index = (index + 1) % window_size # recorremos el index
    average = sum(buffer) / window_size
    return average



# Salimos de la funcion wtf con python
while True:
    raw_signal = generate_emg_signal()
    filtered_signal = sliding_filter(raw_signal)

    # Comparación con el umbral
    if filtered_signal > threshold:
        print("Contraccion detectada!!!: {:.3f} V".format(filtered_signal))
    else:
        print("Reposo: {:.3f} V".format(filtered_signal))
    time.sleep(0.10)

