# Contributing Guidelines for Guajira Coin

¡Bienvenido al proyecto Guajira Coin! Agradecemos tu interés en contribuir al desarrollo de esta criptomoneda de código abierto. Antes de comenzar, por favor, toma un momento para revisar estas pautas de contribución.

## Cómo Contribuir

1. **Billetera Anónima:**
   - Actualmente, la billetera es un bot de Telegram con la dirección del usuario como user_id de la cuenta de Telegram. Necesitamos desarrollar nuestra propia billetera con encriptación y total anonimato. Siéntete libre de contribuir con mejoras en la seguridad y la privacidad de la billetera.

2. **Nodos y Conectividad:**
   - Los nodos actualmente utilizan HTTP para conectarse entre sí. Es necesario migrar al protocolo utilizado por Bitcoin para mejorar la seguridad y la estandarización. Además, la aplicación debe ser capaz de abrir el puerto UPnP para permitir la conexión con otros nodos a través de Internet. ¡Tus contribuciones en este aspecto son vitales para fortalecer la red!

3. **Ampliación de Plataformas Mineras:**
   - En este momento, solo se puede minar con microcontroladores ESP8266. Para hacer Guajira Coin más accesible, necesitamos crear el código minero para ESP32, Arduino Uno, Arduino Nano y Raspberry Pi. Si tienes experiencia en programación para estas plataformas, ¡tu ayuda es invaluable!

4. **Minería en Pools:**
   - Actualmente, cada minero realiza el proceso de minado de forma independiente. Queremos introducir la capacidad de unirse a un pool de minería para mejorar la eficiencia y la equidad en la distribución de recompensas. Contribuciones en la implementación y mejora de la funcionalidad de minería en pools serán muy apreciadas.

## Cómo Contribuir

1. Haz un Fork del Repositorio.
2. Crea una rama para tu contribución: `git checkout -b nombre-de-tu-rama`.
3. Realiza tus cambios y asegúrate de seguir las convenciones de codificación.
4. Añade y realiza un commit de tus cambios: `git commit -m "Descripción del cambio"`.
5. Haz push de tu rama al repositorio en tu Fork: `git push origin nombre-de-tu-rama`.
6. Abre un Pull Request en la rama principal del repositorio original.

## Normas de Codificación

- Sigue las guías de estilo y convenciones de codificación existentes.
- Documenta adecuadamente tu código para facilitar la comprensión.
- Asegúrate de que tus cambios no introduzcan vulnerabilidades de seguridad.

## Comunidad y Comunicación

- Únete a nuestra comunidad en [Telegram Group].
- Participa en discusiones en la [página de issues] para obtener feedback y orientación.

¡Gracias por ser parte de Guajira Coin y por contribuir al futuro de las criptomonedas!

[Telegram Group]: https://t.me/GuajiraCoinCommunity
[página de issues]: https://github.com/tu-usuario/GuajiraCoin/issues
