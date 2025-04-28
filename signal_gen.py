try:
    import utime as time  # Intenta usar utime (MicroPython)
except ImportError:
    import time           # Si falla, usa time (Python normal)
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

muscle_state = "rest"
contraction_duration = 0

def generate_emg_signal_real():
    global muscle_state, contraction_duration

    if muscle_state == "rest":
        if random.random() < 0.05:  # 5% de chance de comenzar contracción
            muscle_state = "contracting"
            contraction_duration = random.randint(5, 15)  # Contracción de 5 a 15 muestras
        return random.uniform(0.4, 0.6)  # Ruido de reposo

    elif muscle_state == "contracting":
        contraction_duration -= 1
        if contraction_duration <= 0:
            muscle_state = "rest"
        return random.uniform(1.2, 2.5)  # Señal de contracción activa

    
window_size = 5 # definimos el tamaño de la ventana
buffer = [0.0] * window_size # creamos un array con ceros del tamaño de la ventana
index = 0 # creamos la variable que regula el index

# creando un umbral de detección:
threshold = 0.8


# creamos un control de contracciones 
contraction_count = 0

# creamos un array para almacenar los bloques de info estructurada:
log = []

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
    index = (index + 1) % window_size # recorremos el index !!! LÍNEA MÁS IMPORTANTE !!! 
    average = sum(buffer) / window_size
    return average

# duncion cuando no usamos la rasp
def get_timestamp():
    try:
        # Si existe time.ticks_ms(), úsalo (MicroPython)
        return time.ticks_ms()
    except AttributeError:
        # Si no existe, estamos en Python normal
        return int(time.time() * 1000)  # segundos * 1000 para tener milisegundos

# Salimos de la funcion wtf con python
while True:
    timestamp = get_timestamp()
    raw_signal = generate_emg_signal_real()
    filtered_signal = sliding_filter(raw_signal)

    # Comparación con el umbral

    #if filtered_signal > threshold:
    #    print("Contraccion detectada!!!: {:.3f} V".format(filtered_signal))
    #    contraction_count += 1
    #else:
    #    print("Reposo: {:.3f} V".format(filtered_signal))
    #time.sleep(0.10)

    # Detecta el estado
    if filtered_signal > threshold:
        state = "contracting"
        contraction_count += 1
    else:
        state = "rest"

    print("Time: {} ms | Filtered Value: {:.3f} V | State: {}".format(timestamp, filtered_signal, muscle_state))

    log.append((timestamp, filtered_signal, state))

    time.sleep(0.1)





