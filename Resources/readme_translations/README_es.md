<!--
*** Official Guajira Coin
*** digovil, 2023-Presente
-->


<h1>
  GUAJIRA-COIN
  <br>
  <a href="https://github.com/Digovil/guajiracoin/blob/master/README.md">
    <img src="https://badgen.net/badge/icon/English?icon=&label" /></a>
  <a href="https://github.com/Digovil/guajiracoin/blob/master/Resources/readme_translations/README_es.md">
    <img src="https://badgen.net/badge/icon/Español?icon=&label" /></a>
  
</h1>
<a href="https://t.me/GuajiraCoinBot">
  <img src="https://badgen.net/badge/icon/Billetera?icon=bitcoin&label" /></a>
<a href="https://github.com/Digovil/guajiracoin/releases/latest">
  <img src="https://img.shields.io/badge/release-latest-ff640a.svg?style=for-the-badge" /></a>
<br>

<h3>
  Guajira-Coin es una criptomoneda que actualmente solo se puede extraer utilizando placas ESP8266.
</h3>

Esta criptomoneda está en proceso de desarrollo y se fundamenta en los principios básicos de Bitcoin, con la distinción de tener un enfoque más eco-amigable en términos de consumo energético. La particularidad de esta iniciativa radica en que su proceso de minado se puede realizar utilizando microcontroladores, lo que la hace más accesible y eficiente. Además de ofrecer la posibilidad de minar la criptomoneda, el proyecto facilita transacciones seguras y sirve como una oportunidad para comprender el funcionamiento de la tecnología blockchain y las criptomonedas.

---

## Contenidos
- [Instalación](#instalación)
- [Cómo empezar](#cómo-empezar)
- [API y Rutas](#api-y-rutas)
- [Contribuciones](#contribuciones)
- [Comunidad y Soporte](#comunidad-y-soporte)
- [Licencia](#licencia)
- [Mantenedores activos del proyecto](#Mantenedores-activos-del-proyecto)

---

## Instalación

### Requisitos previos
- Python 3.x
- Flask
- Microcontroladores ESP8266
- Dependencias especificadas en `requirements.txt`

### Pasos de instalación
1. Clonar el repositorio: `git clone URL_DEL_REPOSITORIO`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Instrucciones adicionales si las hay

---

## Cómo empezar

### Configuración del servidor Blockchain
- Iniciar el servidor: `python app.py`
- El servidor gestionará la cadena de bloques y las transacciones

### Minería con ESP8266
- Configura las credenciales de WiFi en el código del ESP8266
- Agrega la dirección de tu billetera
- Sube el código a tu ESP8266
- El dispositivo empezará a minar automáticamente, interactuando con el servidor

---

## API y Rutas

Descripción de las principales rutas y métodos de la API del servidor, como:
- `GET /chain`: Obtiene la cadena de bloques actual
- `POST /transactions/new`: Añade una nueva transacción
- `POST /mine`: Realiza la minería de un nuevo bloque

---

## Contribuciones

Las contribuciones son lo que hacen que la comunidad de código abierto sea un lugar increíble para aprender, inspirarse y crear.<br>
Cualquier contribución que haces al proyecto de Guajira-Coin son gratamente apreciadas.

¿Como ayudar?

*   Bifurca el proyecto (fork)
*   Crea tu rama de desarrollo
*   Sube tus cambios (commit)
*   Asegúrate de que todo funciona como debería
*   Abre una petición de subida (pull request)

---

## Comunidad y Soporte

Únete a nuestra comunidad en [Discord](https://discord.gg/yAW2ddkhuk) para obtener soporte, discutir y compartir ideas sobre el proyecto.

---

## Licencia

Guajira-Coin está distribuído principalmente bajo la licencia MIT. Mira el archivo `LICENSE` para más información.
Algunos archivos de terceros incluídos pueden tener licencias diferentes - por favor checa sus archivos `LICENSE` (usualmente en la parte superior del codigo fuente).

---

## Mantenedores activos del proyecto

*   [@Digovil](https://github.com/Digovil/) - dgonzalezv@uniguajira.edu.co (Desarrollador, fundador del proyecto)
*   Luz Moronta Iguaran - lmoronta@uniguajira.edu.co (Desarrolladora, cofundadora del proyecto)

<hr>

Enlace del Proyecto: [https://github.com/Digovil/guajiracoin/](https://github.com/Digovil/guajiracoin/)
