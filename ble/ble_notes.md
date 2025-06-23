# Libraries

```cpp
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>
```

# Variables

1. BLE Object pointer:
   It is a pointer because BLECharacteristic returns a pointer from "createCharacteristic()"

2. Connection status flag:
   boolean that indicates wether the device is connected.

### UUIDS

    Universally Unique Identifier. Cadena de 128 bits en hexadecimal.
        1. Service -> el conjunto de info
        2. Characteristic -> chunk de info

Sintaxis:

```cpp
    #define UUID "value"
```

    # define: actúa antes de que el código se compile (preprocesador). No ocupa espacio en memoria.

## Métodos

Tomamos la clase BLEServerCallbacks y hacemos un tipo "override" de sus métodos (están vacíos por defecto para que hagamos esto).

```cpp
    class MyServerCallbacks: public BLEServerCallbacks {
        void onConnect(BLEServer* pServer){
            deviceConnected = true;
            // más cosas de debbugging
        }

        void onDisconnect(BLEServer* pServer){
            deviceConnected = false;
        }
    };
```

## Setup

Lo que va en la función void setup()

1. Resetear conexiones

```cpp
    BLEDevice::deinit(true);
```

Fuerza limpieza de conexiones accediendo a la función estática "deinit()"

2. Inicializar device.

```cpp
    BLEDevice::init("XIAO-EMG");
```

Accede al método "init" de la clase BLEDevice mediante el operador "::" (operador de resolución) PERO sin la necesidad de crear una instancia para usarlo.

3.  Crear server

```cpp
    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
```

Creamos un pointer al objeto del server BLE y le asignamos los métodos que overrideamos: onConnect(), onDisconnect().

// ¿Qué es un server?

4. Crear service

```cpp
    BLEService *pService = pServer->createService(SERVICE_UUID);
```

Creamos un pointer al objeto de BLEService. Este Service representa el conjunto de datos o características a enviar, como un paquete 📦

5. Crear Carachteristic

```cpp
    pCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID,           BLE_Characteristic::PROPERTY_NOTIFY);
```

Aquí estamos usando el operador de resolución "::" de la clase BLECharacteristic, porque, si nos damos cuenta, como tal no estamos creando un nuevo objeto "BLECharacteristic" en ninguna parte.

// ¿Por qué la sintaxis de crear una characteristic no es igual a la de crear un Service?

6. Añadir un descriptor a la característica.

```cpp
    pCharacteristic->addDescriptor(new BLE2902());
```

Accedemos al método addDescriptor() e inicializamos un nuevo objeto BLE2902(), esto significa que el tipo de conexión será BLE2902.

7. Inicializar o activar el servicio.

   1. Start:

   ```cpp
       pService->start();
   ```

   2. Notify
      Es alertar a la comunidad BLE que estamos listos y ponemos nuestro número de contacto!!

   ```cpp
       pServer->getAdvertising()->start();
   ```

   // ¿por qué llamar al server y no al device? -> nuestro server representa a nuestro device. Por eso usamos el operador de resolución.

## Loop

A grandes rasgos, revisamos nuestra flag de conexión "deviceConnected" y ejecutamos la acción de enviar datos con otros métodos de lo que estamos enviando, los items dentro de nuestro paquete: characteristics.

```cpp
    if (deviceConnected){
        static int value = 0; // static para que pueda cambiar en cada iteración.
        String message = "Lectura" + String(value++);

        pCharacteristic->setValue(message.c_str());
        pCharacteristic->notify();

        delay(1000);
    }
```

# ¿Cómo funciona la función c_str()"

Es un método de String que devuelve un puntero const char. ES DECIR, una string a su mínima y rudimentaria expresión -> cadena de texto (datos binarios) + dirección en memoria.

Para enviar cualquier texto, es necesario usar este método.
