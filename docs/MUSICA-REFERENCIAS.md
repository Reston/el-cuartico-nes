# Música de las referencias · v0.13.0

La nueva música es un arreglo instrumental para NES de las grabaciones entregadas
por el usuario. Se conservan frases cortas, su contorno melódico y una reducción
del acompañamiento. No se reproducen las voces ni el audio M4A dentro del cartucho.

| Destino | Referencia | Frase tomada como base | Bucle NES |
| --- | --- | --- | --- |
| Menú y estudio compartido | elcuartico_song_2.m4a | Aproximadamente 0:09,6–0:19,2; bajo del patrón de 0:19,2–0:28,8 | Cuatro compases, 100 BPM, ~9,6 s |
| Estefania, ambos episodios | elcuartico_song_3.m4a | Aproximadamente 0:48–0:57,6 | Cuatro compases, 120 BPM, ~8 s |

El fraseo del menú se eligió por su motivo corto y repetido, que permite entrar
directamente en la música sin esperar la introducción. En Estefania se usa una
frase melódica del tramo central. El ritmo original está cerca de 100 BPM; su
arreglo se acelera para conservar la sincronía y dificultad existentes del juego.
Los tres actos comienzan en compases distintos y alternan el timbre del pulso.

La melodía y el bajo suben una octava para colocarse en un registro más claro en
altavoces pequeños. Las notas se reducen a semicorcheas; las ligaduras evitan
repetir el ataque de una nota larga. La percusión se simplifica al canal de ruido.

La salida nueva todavía necesita escucharse en la R36S física.

## Partitura y reproducción

[La partitura editable](../assets/song-arrangements.json) registra notas, duraciones,
patrón de bajos, percusión, fragmentos de referencia y hashes de los dos originales.
`./build.ps1` genera sus tablas automáticamente. Las grabaciones originales no se
incluyen en el repositorio y no hacen falta para compilar.

Para reducir las grabaciones se contrastaron estimaciones de tempo por bandas,
notas extraídas con [Basic Pitch](https://github.com/spotify/basic-pitch) y una
separación de acompañamiento repetido con [librosa](https://librosa.org/).
Es una reducción musical revisada, no una transcripción exacta de todas las voces.

## Validación de la entrega

**808 comprobaciones superadas:** trece suites FCEUmm y cinco Mesen. Incluyen las
dos campañas, las seis variantes musicales, notas y sostenidas, pausa/reanudación,
ligaduras sin reiniciar el oscilador y comprobación de frecuencias reales de la APU.
El audio PCM se comprueba en memoria y no alcanza saturación digital. La compilación final coincide
byte a byte con la ROM probada; conserva 128 KiB PRG y 256 KiB CHR.
