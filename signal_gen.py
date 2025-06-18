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


# función de adquisición de archivo .csv con datos 
def save_log_to_csv(filename, log_data):
    """     
        Recibe EMG data y la guarda en un archivo .csv
        Donde:
        - filename: nombre del archivo a guardar.
        - log_data: lista/array de datos a guardar

        Step by step:
            open(): abre o crea un archivo.
                "w" como parámetro significa "modo escritura".
            este archivo abierto se llama "file" localmente.

            file.write(): escribe la primera línea (los encabezados) del archivo.

            for entry in log_data:
                for: recorre cada elemento en el array.
                    - cada elemento se guarda localmente en la variable "entry"
                        cada entry es un tuple.
                    - timestamp, value, state = entry -> deshace el tuple.
            
            formatting:
                escribe una línea para cada registro de log_data.
    
    """
    with open(filename, "w") as file:
        file.write("Timestamp_ms,Filtered_Value_V,State\n")  # Encabezados CSV
        for entry in log_data:
            timestamp, value, state = entry
            file.write("{},{:.3f},{}\n".format(timestamp, value, state))         
         
# función para generar distintos files
def generate_filename(base_name="emg_log"):
    try:
        # MicroPython no tiene datetime completo, simulamos con ticks_ms
        now = get_timestamp()
        seconds = now // 1000
        minutes = (seconds // 60) % 60
        hours = (seconds // 3600) % 24
        day = 1  # No podemos saber el día real sin RTC
        month = 1  # Idem

        filename = "{}_{}_{}_{}_{}.csv".format(base_name, day, month, hours, minutes)
    except:
        # Si estamos en PC (Python normal), usamos datetime real
        import datetime
        now = datetime.datetime.now()
        filename = "{}_{}_{}_{}_{}.csv".format(base_name, now.day, now.month, now.hour, now.minute)
    
    return filename

# Salimos de la funcion wtf con python

try:
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

        # guardar en mi log para further .csv
        log.append((timestamp, filtered_signal, state))

        time.sleep(0.1)
except KeyboardInterrupt:
    filename = generate_filename()
    print("\n🛑 Adquisición detenida. Guardando datos en archivo...")
    save_log_to_csv(filename, log)
    print("✅ Datos guardados exitosamente en 'emg_log.csv'.")







