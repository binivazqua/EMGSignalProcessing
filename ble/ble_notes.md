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
    Define: actúa antes de que el código se compile (preprocesador). No ocupa espacio en memoria. 


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





