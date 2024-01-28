#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <bearssl/bearssl.h>
#include <ArduinoJson.h>

const char *ssid = "Claro_01919C";
const char *password = "P5K8H2P3B2A2";
const char *serverAddress = "192.168.20.21:8000"; // Reemplaza con la dirección de tu servidor

// const char *targetPrefix = "0000"; // Requiere 4 ceros iniciales en el hash
const int SHA1_HASH_SIZE = 20;     // Longitud del hash SHA-1 en bytes

  // Obtener transacciones pendientes del servidor
WiFiClientSecure client;

void setup()
{
  client.setInsecure();
  Serial.begin(115200);
  while (!Serial)
  {
    delay(10);
  }

  // Conexión a la red WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a la red WiFi");

  mine();
}

void loop()
{
  // El bucle principal no hace nada en este ejemplo
}

void cutTargetPrefix(String &payload, String &targetPrefix) {
  DynamicJsonDocument jsonDocument(1024); // Tamaño del documento JSON, ajusta según sea necesario
  DeserializationError error = deserializeJson(jsonDocument, payload);

  if (error) {
    Serial.print("Error al deserializar JSON: ");
    Serial.println(error.c_str());
    return;
  }

  // Obtener el valor de "targetPrefix" y asignarlo a la variable
  targetPrefix = jsonDocument["targetPrefix"].as<String>();

  // Eliminar el campo "targetPrefix" del JSON
  jsonDocument.remove("targetPrefix");

  // Serializar el JSON modificado de nuevo a un String
  serializeJson(jsonDocument, payload);
}


void mine()
{

  while (true)
  {


    HTTPClient http;
    String url = "https://" + String(serverAddress) + "/transactions/get"; // Cambia a HTTPS
    http.begin(client, url);
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200)
    {
      
      String payload = http.getString();
      String targetPrefixValue;

      // Obtener y eliminar targetPrefix del JSON
      cutTargetPrefix(payload, targetPrefixValue);

      Serial.println("Dificultad: " + targetPrefixValue);
      Serial.println("Obteniendo respuesta del servidor:");
      Serial.println(payload);
      
      // Realizar la minería localmente y obtener el proof de trabajo
      unsigned long nonce = 0;

      while (true)
      {
        String combinedData = payload + String(nonce);
        String hash = calcularPruebaDeTrabajo(combinedData);

        if (hash.startsWith(targetPrefixValue))
        {
          Serial.println("Prueba de trabajo encontrada!");
          Serial.print("Hash: ");
          Serial.println(hash);
          Serial.print("Nonce: ");
          Serial.println(nonce);

          // Enviar el proof de trabajo al servidor
          if (enviarProofDeTrabajo(hash, nonce))
          {
            Serial.println("Proof de trabajo enviado con éxito.");
          }
          else
          {
            Serial.println("Error al enviar el proof de trabajo.");
          }

          break;
        }

        nonce++;

        // Introducir un pequeño retraso para permitir que el sistema atienda otras tareas
        delay(1);
      }
    }
    else
    {
      Serial.print("Error al obtener transacciones. Código de respuesta: ");
      Serial.println(httpResponseCode);
    }

    http.end();

    delay(5000); // Espera 5 segundos antes de comenzar una nueva prueba de trabajo
  }
}

String calcularPruebaDeTrabajo(String data)
{
  br_sha1_context sha1_ctx_base;
  br_sha1_init(&sha1_ctx_base);
  br_sha1_update(&sha1_ctx_base, data.c_str(), data.length());

  uint8_t hash[SHA1_HASH_SIZE];
  br_sha1_out(&sha1_ctx_base, hash);

  String hashString = "";
  for (int i = 0; i < SHA1_HASH_SIZE; i++)
  {
    char hex[3];
    sprintf(hex, "%02x", hash[i]);
    hashString += hex;
  }

  return hashString;
}

bool enviarProofDeTrabajo(String hash, unsigned long nonce)
{


  HTTPClient http;
  String url = "https://" + String(serverAddress) + "/mine"; // Cambia a HTTPS
  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  // Construir el cuerpo JSON con el proof de trabajo y la dirección del minero
  DynamicJsonDocument jsonDocument(256); // Ajusta el tamaño según tus necesidades
  jsonDocument["proof"] = hash;
  jsonDocument["miner_address"] = "DirecciónDelMinero";

  String json;
  serializeJson(jsonDocument, json);

  int httpResponseCode = http.POST(json);

  if (httpResponseCode == 200)
  {
    String payload = http.getString();
    Serial.println("Respuesta del servidor:");
    Serial.println(payload);
    return true;
  } else if (httpResponseCode == -1) {
    Serial.print("Error en la solicitud HTTPS. Código de error: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
    return false; // Agregar este retorno

  }else
    {
      Serial.print("Error al enviar proof de trabajo. Código de respuesta: ");
      Serial.println(httpResponseCode);
      return false;
    }
  http.end();
}
