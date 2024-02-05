/*

   _____             _ _ _                   _____      _       
  / ____|           (_|_|_)                 / ____|    (_)      
 | |  __ _   _  __ _ _ _ _ _ __ __ _ ______| |     ___  _ _ __  
 | | |_ | | | |/ _` | | | | '__/ _` |______| |    / _ \| | '_ \ 
 | |__| | |_| | (_| | | | | | | (_| |      | |___| (_) | | | | |
  \_____|\__,_|\__,_| |_|_|_|  \__,_|       \_____\___/|_|_| |_|
                   _/ |                                         
                  |__/                                          
  Official code for ESP8266 boards                   version 1.0

  Guajira-Coin Team & Community 2023-2024 © MIT Licensed
  https://www.guajiracoin.online/
  https://github.com/Digovil/guajiracoin

  Si no sabe por dónde empezar, visite el sitio web oficial y navegue hasta
  la página de introducción. ¡Diviértete minando!
*/


#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <bearssl/bearssl.h>
#include <ArduinoJson.h>
#include <AdafruitIO_WiFi.h>

#define IO_USERNAME  "io_username"
#define IO_KEY       "io_key"

const char *ssid = "ssid";
const char *password = "password";
const char *serverAddress = "digovil.pythonanywhere.com"; // Reemplaza con la dirección de tu servidor
const char *miner_address = "direccion_billetera";

const int SHA1_HASH_SIZE = 20;     // Longitud del hash SHA-1 en bytes

// Obtener transacciones pendientes del servidor
WiFiClientSecure client;
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, ssid, password);
AdafruitIO_Feed *Consola = io.feed("name_feed");


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
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
 
}

void loop()
{
    digitalWrite(LED_BUILTIN, LOW);
    mining();
    delay(10);
}



void mining() {


  
    HTTPClient http;
    io.run();

    String url = "https://" + String(serverAddress) + "/transactions/get"; // Cambia a HTTPS
    http.begin(client, url);
    digitalWrite(LED_BUILTIN, HIGH); 
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200)
    {
      digitalWrite(LED_BUILTIN, LOW);
      String payload = http.getString();
      String targetPrefixValue;
      http.end();

      // Obtener y eliminar targetPrefix del JSON
      cutTargetPrefix(payload, targetPrefixValue);

      Consola->save("Dificultad: " + targetPrefixValue);
      Consola->save("Obteniendo respuesta del servidor...");

      // Realizar la minería localmente y obtener el proof de trabajo
      unsigned long nonce = 0;

      while (true)
      {
        String combinedData = payload + String(nonce);
        String hash = calcularPruebaDeTrabajo(combinedData);
        

        if (hash.startsWith(targetPrefixValue))
        {
          digitalWrite(LED_BUILTIN, HIGH); 
          Consola->save("Prueba de trabajo encontrada!");

          // Enviar el proof de trabajo al servidor
          if (enviarProofDeTrabajo(combinedData, nonce))
          {

            Consola->save("Proof de trabajo enviado con éxito.");
          }
          else
          {
            Consola->save("Error al enviar el proof de trabajo.");
          }

          break;
        }

        nonce++;

        delay(10);
      }
    }else if (httpResponseCode == -1) {
      Consola->save("Error en la solicitud HTTPS. Código de error: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }else {
      Consola->save("Error al obtener transacciones. Código de respuesta: ");
      Serial.println(httpResponseCode);
    }

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

bool enviarProofDeTrabajo(String combinedData, unsigned long nonce)
{


  HTTPClient http;
  String url = "https://" + String(serverAddress) + "/mine"; // Cambia a HTTPS
  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  // Construir el cuerpo JSON con el proof de trabajo y la dirección del minero
  DynamicJsonDocument jsonDocument(256); // Ajusta el tamaño según tus necesidades
  jsonDocument["combinedData"] = combinedData;
  // Aquí colocas la dirección que se te da al loguearte en el bot
  jsonDocument["miner_address"] = String(miner_address);
  jsonDocument["nonce"] = nonce;

  String json;
  serializeJson(jsonDocument, json);

  int httpResponseCode = http.POST(json);

  if (httpResponseCode == 200)
  {
    String payload = http.getString();
    Consola->save("Respuesta del servidor:");
    Consola->save(payload.c_str());
    return true;
  } else if (httpResponseCode == -1) {
    Consola->save("Error en la solicitud HTTPS. Código de error: ");
    Consola->save(http.errorToString(httpResponseCode).c_str());
    return false; // Agregar este retorno

  }else
    {
      Serial.print("Error al enviar proof de trabajo. Código de respuesta: ");
      Serial.println(httpResponseCode);
      return false;
    }
  http.end();
}
