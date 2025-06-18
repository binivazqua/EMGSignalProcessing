import serial
import time
import csv

# Crear puerto 
ser = serial.Serial('/dev/tty.usbmodem11201', 115200)

filename = 'rasp_data.csv'
window_size = 5
index = 0
buffer = [0.0] * window_size
threshold = 0.3
muscle_state = "rest"

def sliding_filter(value):
    """
        Func que recibirá un nuevo valor cada 10ms y:
            - Lo guardará en el buffer
            - Actualiza el índice
            - Calcula el promedio
            - Devuelve el resultado

    """
    global index 
    buffer[index]
    index = (index + 1) % window_size
    average = sum(buffer) / window_size
    return average

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
                print(f"Muscle state: {muscle_state}, Voltage: {voltage:.2f} V, Filtered Value: {sliding_filter(raw_value):.2f} V")
                writer.writerow([round(timestamp, 2), round(voltage, 2), muscle_state])
                # buffer[index] = filtered_value
            except ValueError:
                pass

