import serial
import time
import csv

# Crear puerto 
ser = serial.Serial('/dev/tty.usbmodem1401', 115200)

filename = 'rasp_data.csv'
window_size = 5
index = 0
buffer = [0.0] * window_size
threshold = 0.3
muscle_state = "rest"

def sliding_filter(value):
    """
    Applies a sliding window average filter to a stream of incoming values.

    Each time a new value is received, it is stored in a circular buffer of fixed size (`window_size`).
    The function updates the buffer index, computes the average of the current buffer contents,
    and returns the result. This is typically used for smoothing noisy signals, such as EMG data.

    Parameters:
        value (float): The new value to add to the sliding window buffer.

    Returns:
        float: The current average of the values in the buffer.

    Example:
        >>> window_size = 3
        >>> buffer = [0.0] * window_size
        >>> index = 0
        >>> sliding_filter(1.0)
        0.3333333333333333
        >>> sliding_filter(2.0)
        1.0
        >>> sliding_filter(3.0)
        2.0
        >>> sliding_filter(4.0)
        3.0
    
        Func que recibirá un nuevo valor cada 10ms y:
            - Lo guardará en el buffer
            - Actualiza el índice
            - Calcula el promedio
            - Devuelve el resultado
    """
    global index 
    buffer[index] = value
    index = (index + 1) % window_size
    average = sum(buffer) / window_size
    return average

def sliding_filter_explained(value):
    global index
    print(f"Índice antes: {index}")
    buffer[index] = value
    print(f"Guardando {value} en buffer[{index}]")
    # Aquí usamos el módulo para que el índice vuelva a 0 cuando llegue a window_size
    index = (index + 1) % window_size
    print(f"Índice después: {index} (por módulo: ({index - 1} + 1) % {window_size})")
    print(f"Buffer actual: {buffer}\n")
    return sum(buffer) / window_size

# Simulación de llegada de datos
datos = [10, 20, 30, 40, 50]
for dato in datos:
    promedio = sliding_filter(dato)
    print(f"Nuevo dato: {dato}, Promedio: {promedio}\n{'-'*40}")

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


with open(generate_filename(), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['timestamp', 'emg_voltage', 'muscle_state'])

    start_time = time.time()
    while time.time() - start_time < 20: # -> 10 secs
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            timestamp = time.time() - start_time
            try:
                raw_value = int(line)
                voltage = raw_value * (3.3 / 4095.0)
                
                if voltage > threshold:
                    muscle_state = "active"
                else:
                    muscle_state = "rest"
                print(f"Muscle state: {muscle_state}, RawValue: {raw_value}, Voltage: {voltage:.2f} V, Filtered Value: {sliding_filter(voltage):.2f} V")
                writer.writerow([round(timestamp, 2), round(voltage, 2), muscle_state])
                
                
            except ValueError:
                pass

