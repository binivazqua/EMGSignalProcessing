from machine import UART, Pin, ADC 
import time
import ujson

# Configuración del UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) # se ajusta el pin

# Configuración del ADC
adc = ADC(Pin(26))  # Pin ADC para lectura de datos analógicos

# Parámetros de procesamiento
window = []
window_size = 50
summary_interval_ms = 500
last_summary_time = time.ticks_ms()
threshold = 3.0



def sliding_average(value):
    """
    Applies a sliding window average filter to a stream of incoming values.
    
    Each time a new value is received, it is stored in a circular buffer of fixed size (`window_size`).
    The function updates the buffer index, computes the average of the current buffer contents,
    and returns the result. This smooths noisy signals, such as EMG data.
    
    Parameters:
        value (float): The new value to add to the sliding window buffer.
    
    Returns:
        float: The current average of the values in the buffer.
    """
    global window, window_size

    if len(window) >= window_size: 
        # if window is full, remove the oldest value
        window.pop(0)
    # append the new value to the window
    window.append(value)
    return sum(window) / len(window)

while True:
    # Leer el valor del ADC
    adc_value = adc.read_u16()  >> 4  # Convertir a un rango de 0 a 4095 (12 bits) (lo divide por 16 o desplaza 4 bits a la derecha)
    # Convertir el valor ADC a voltaje (0-3.3V)
    voltage = adc_value * (3.3 / 4095)  # Convertir a voltaje (0-3.3V)
    # Aplicar sliding average
    avg_value = sliding_average(voltage)
    # Obtener el tiempo actual
    now = time.ticks_ms()

    # Verificar si ha pasado el intervalo de resumen: "ahora menos último tiempo de resumen" es mayor o igual al intervalo?"
    if now - last_summary_time >= summary_interval_ms:
        # Crear paquetito de datos
        data = {
            "avg_value": avg_value,
            "adc_value": adc_value,
            "min_value": min(window) if window else 0, # siempre agregar un fail safe si "window" está vacío.
            "max_value": max(window) if window else 0,
            "state": "active" if avg_value > threshold else "rest",
        }
        # Convertir la data a un JSON 
        json_data = ujson.dumps(data)
        # Enviar los datos por UART
        uart.write(json_data + '\n')
        #print(f"valor ADC: {adc_value}, Voltaje: {voltage:.2f}V, Promedio: {avg_value:.2f}V, Estado: {data['state']}")
        print(f"Enviado: {json_data}")
        # Actualizar el tiempo WOWOWOW
        last_summary_time = now
    
    # Esperar un poco antes de la siguiente lectura
    time.sleep_ms(4) # mantiene los 250Hz de muestreo (4ms por lectura)
