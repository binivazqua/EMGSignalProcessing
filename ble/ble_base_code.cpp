
// #include <BLEDevice.h>
// #include <BLEUtils.h>
// #include <BLEServer.h>
// #include <BLE2902.h>

// // variables iOT
// BLECharacteristic *pCharacteristic; // puntero al BLE object -> createCharacteristic()
// bool deviceConnected = false; // flag de conexión

// // UUIDS = Universally Unique Identifier -> 128bits en hexadecimal.
// // variablesn't
// #define SERVICE_UUID  "2E18CC93-EFBE-4927-AC92-0D229C122383" // estante
// #define CHARACTERISTIC_UUID  "13909B07-0859-452F-AB6E-E5A4BC8D9DF4" // libro

// // Callbacks de conexión derivados de BLEServerCallbacks
// class MyServerCallbacks: public BLEServerCallbacks {

//   // overrideando metodos para actualizar mi flag
//   void onConnect(BLEServer* pServer) {
//     deviceConnected = true;
//   }

//   void onDisconnect(BLEServer* pServer) {
//     deviceConnected = false;
//   }
// };

// void setup() {
//   // put your setup code here, to run once:
//   Serial.begin(115200);
//   // Inicializar device
//   BLEDevice::deinit(true);  // Fuerza limpieza de sesiones BLE previas
//   BLEDevice::init("XIAO-EMG"); // ACCEDER AL MÉTODO INIT sin crear una instancia
 


//   // Crear server con las funciones que overrideamos. Servidor -> transmite. Cliente -> recibe
//   BLEServer *pServer = BLEDevice::createServer();
//   pServer->setCallbacks(new MyServerCallbacks());

//   // Crear service -> conjunto de características a otorgar/transmitir al cliente.
//   BLEService *pService = pServer->createService(SERVICE_UUID); 

//   // Crear característica -> datos individuales a enviar.
//   pCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID, BLECharacteristic::PROPERTY_NOTIFY); // Usamos PROPERTY_NOTIFY para enviar datos automáticamente sin que el cliente los pida.

//   // Añadir descriptor a la característica -> describe cómo usarla, permite que el cliente la interprete, acceda a ella.
//   pCharacteristic->addDescriptor(new BLE2902()); 

//   // Activar servicio y mostrar dispositivo por BLE
//   pService->start();
//   // "holis, soy XIAO-EMG!!"
//   pServer->getAdvertising()->start();

//   // Debug line:
//   Serial.println("Esperando conexión BLE...");



// }

// void loop() {
//   // put your main code here, to run repeatedly:

//   // Lógica de envío de datos:
//   if (deviceConnected) {
//     // static para que la variable cambie al entrar al loop cada vez.
//     static int value = 0;
//     String message = "Lectura: " + String(value++);

//     pCharacteristic->setValue(message.c_str()); // convierte el mensaje a un objeto que se puede enviar sin pex.
//     pCharacteristic->notify(); // "enviar"

//     Serial.println("Datos enviados correctamente");

//     delay(1000);
//   }


//   // 
// }
