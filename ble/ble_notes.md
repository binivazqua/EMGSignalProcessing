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




