.. _mining:

Minar con Guajira-Coin
=========================

Aprende cómo minar Guajira-Coin y contribuir a la red.

.. important::

    El estado de la criptomoneda es funcional, pero no es operativa, aún se encuentra en desarrollo.  


Requisitos 
---------------

1. ESP8266
2. Arduino IDE
3. Librerías: ArduinoBearSSL, ArduinoJson

Inicio
---------------

1. Descarga y ejecuta el archivo MinerESP8266
2. Configuración de la red wifi, sólo admite Wifi 2.4GHz:

:code:`ssid = "Colocas tu nombre de red";`
    

:code:`password = "Colocas tu contraseña de red";`

4. Crear una billetera: Para esto simplemente ingresa al bot de 
telegram https://t.me/GuajiraCoinBot Billetera de Guajira-Coin. 
le das /start, luego /registrar y posteriormente /login y te dará 
una bienvenida con la respectiva dirección de tu billetera.
5. Configuración de la dirección del minero: 

:code:`miner_address = "colocas la dirección de tu minero";`
    
6. Flashea el ESP8266 y listo!

