# Desarrollo

## Cartucho y código

El juego usa un encabezado iNES, mapper **MMC5 (5)**, 128 KiB de PRG y 256 KiB de
CHR. Hay 54 bancos gráficos de 4 KiB ocupados. La memoria de batería no se utiliza.

- `src/game.c`: estados, entrada, campaña y minijuegos.
- `src/start.s`: arranque 6502, NMI, DMA de sprites y configuración MMC5.
- `src/music.h`: temas y efectos de la APU.
- `src/nes.cfg`: mapa de memoria de cc65.
- `assets/likeness.py`: personajes y poses mediante píxeles indexados.
- `assets/quality.py`: escenas, animaciones, tiles y atributos MMC5.
- `assets/generate.py`: punto de entrada para generar los recursos gráficos.
- `src/presentation.h`: ayuda, pausa y resultados.
- `src/episode2.h`: misiones del directo, objetos y transición de campaña.
- `assets/presentation.py`: tarjeta gráfica compartida por estas pantallas.
- `assets/character_intros.py`: pósteres de Chuchito y The Lion Queen.

Los recursos se generan sin leer fotografías externas. Las imágenes del README
son ilustración y capturas del juego; no son necesarias para compilar.

## Renderizado

El menú cambia sus etiquetas y marcadores durante vblank; no se vuelve a cargar
la pantalla al elegir otro personaje. Las animaciones intercambian bancos CHR.
Las personas de Daniel usan tiles de fondo, reservando sprites para el cursor,
la lupa y los efectos. Sus caras permanecen visibles gracias a la prioridad de
fondo de las esquinas de selección.

Los paneles de reparación comparten el juego de tiles del estudio. El temporizador
de la secuencia de memoria es de 16 bits: cuatro pasos de 80 cuadros suman 320.
El objetivo del mezclador cambia entre aciertos y no depende de una posición fija.

## Pruebas

Primero compila con `./build.ps1`. `tools/test_all.py` ejecuta doce suites de
FCEUmm; `--mesen` añade cuatro suites independientes con Mesen: campaña original,
restauración de imagen, campaña completa de dos episodios y tarjetas/ayuda. Los resultados se
guardan en `build/`, junto a la ROM de trabajo, símbolos y capturas. Cada suite
falla con un código distinto de cero si detecta una regresión.

No se incluyen ejecutables de emuladores, bibliotecas DLL, compiladores ni archivos
ZIP de instalación. `tools/bootstrap.py --test-tools` prepara esos recursos localmente.

## Publicar una versión

1. Actualiza `VERSION` y los enlaces e instrucciones de la entrega.
2. Compila y ejecuta las pruebas correspondientes al cambio.
3. Guarda la ROM anterior en una carpeta fuera del repositorio.
4. Ejecuta `python tools/package.py`.
5. Comprueba que `dist/` contiene solo la ROM actual, `LEEME.txt` y `SHA256.txt`.

El empaquetador rechaza la publicación si encuentra otra ROM en `dist/`: nunca
borra una entrega anterior automáticamente. El código fuente se distribuye por Git;
no se guarda un ZIP del propio repositorio dentro de sí mismo.

## Alcance de la validación

Las pruebas de escritorio cubren FCEUmm y Mesen CE. La ROM actual necesita una
prueba adicional en hardware portátil; no debe confundirse el funcionamiento
del emulador de escritorio con una prueba física en R36S o Retroid.

## Ajuste de dificultad en v0.9.2

Los cuatro paneles de Chucho congelan segundos, fracción de segundo y plazos de
averías. El reloj continúa al cerrar o completar un panel; la interfaz muestra
SIN LÍMITE durante la reparación. La prueba de permanencia supera 80 segundos
sin consumir recursos y verifica la reanudación al regresar al estudio.

## Edición de prueba v0.10.0

La rama `feature/episode-remix` añade un estado LOUNGE para recorrer el estudio.
HUB conserva el menú y su actualización atómica. La franja de contexto tiene
32 caracteres en la fila 3 y se publica en NMI; en Daniel, la referencia facial
ocupa las filas 4 y 5 para dejar libre esa franja y la navegación inferior.

Los eventos se barajan al comenzar Chucho y aparecen tras las reparaciones 3, 6
y 9. Cada uno activa una estación con 18 segundos de plazo exterior. El plazo,
el reloj y los corazones permanecen congelados al abrir cualquier panel. Un evento
vencido limpia su estado visual. Los errores del panel solo afectan la medalla.

Los tres actos usan pistas 2, 6 y 7 a 15 cuadros por corchea. Cambian al llegar
a 7 y 13 aciertos, vacían la cola y cuentan 120 cuadros antes de seguir. Sus
paletas cambian dentro de NMI, sin cargar una pantalla ni interrumpir el pulso.

Los distritos impares reflejan tanto la calle como sus posiciones y atributos.
Remix ocupa hasta las 24 plazas disponibles; conserva la selección por distancia,
la persistencia al volver y el límite de ocho sprites por línea.

`episode_test.py` recorre el estudio y completa las campañas normal y remix con
entradas de control; comprueba eventos, premios, medallas, actos, audio y final.
La ROM conserva el tamaño del cartucho. BOOTDATA aloja tablas pequeñas en el
banco fijo; el enlazador comprueba los límites restantes de PRG y RAM.

## Arte de Daniel v0.10.1

La búsqueda usa seis figuras de 16 × 24 píxeles independientes de los sprites
de Chucho y Estefania. Sus 36 tiles ocupan el final de cada banco de plaza;
`search_person` publica seis tiles contiguos por figura. El banco 46 contiene los
sprites de búsqueda y la nueva referencia facial. La lupa conserva su banco 25,
con la misma referencia pequeña. Los demás juegos mantienen sus bancos anteriores.

Las siete áreas respetan el máximo de 220 tiles de escenario por banco. Los
posibles escondites se despejan antes de codificar el fondo, también para Remix;
los atributos de 16 × 16 y los caminos reflejados conservan sus posiciones.

## Intro y retratos v0.10.2

SEARCH_INTRO (7) muestra una tarjeta estática antes de iniciar o reintentar
la búsqueda. A/Start carga la plaza, B vuelve al menú; el reloj no avanza.
La intro usa CHR 47/48, 495 tiles y atributos MMC5 de 8 × 8. `ex_on=2` evita que
la animación de retratos escriba en su ExRAM; `ex_on=1` mantiene el menú animado.

El mapa, los atributos y la paleta de la intro ocupan el banco PRG 0, antes libre.
El cargador se ejecuta en el banco fijo con NMI/renderizado desactivados, mapea
ese recurso en $8000 y restaura el banco 12 antes de regresar a C. El tamaño del
cartucho sigue siendo 128 KiB PRG y 256 KiB CHR. Las pruebas incluyen salir,
reintentar, resetear desde la tarjeta y completar la campaña en ambos emuladores.

`menu_portrait` es independiente de los sprites de juego y de la lupa. Solo cambia
los retratos compartidos por menú, resultados y final, conservando sus parpadeos.


## Presentación v0.11.0

HELP (8) muestra instrucciones opcionales desde arriba en el menú. Las flechas
cambian el personaje de la ayuda y A/Start inicia su juego respetando los sellos
ya conseguidos. Durante una pausa, Select abre los controles del juego o del
panel de reparación actual; Select/B regresa a la pausa y Start continúa.

La tarjeta usa el banco CHR 49, fuentes ASCII fijas y atributos normales de
16 × 16. Su cabecera distingue pausa, éxito y derrota mediante color. RESULT
usa esta tarjeta para mostrar el objetivo, puntos, errores y progreso del episodio.

Al pausar, una rutina con renderizado desactivado conserva los 1024 bytes de la
tabla de nombres y atributos en ExRAM y las 32 entradas de paleta en RAM. Las
pantallas de ayuda no escriben sobre esa copia. Al continuar se restauran la
imagen, las paletas y los bancos gráficos sin regenerar el mundo ni el puzle.
La NMI omite la iluminación musical mientras se muestra la tarjeta de pausa.

Los cuatro mapas de distrito se movieron de la ventana de código a la parte
libre del banco PRG 0, junto a la tarjeta y la intro de Dany. `load_resource`
corre en el banco fijo, carga el mapa y sus atributos y restaura el banco 12
antes de volver a C. El cartucho conserva 128 KiB PRG y 256 KiB CHR.

`presentation_test.py` usa solo controles para comprobar navegación, relojes,
silencio, reintentos y los cuatro puzles. `presentation_mesen.lua` compara los
1024 bytes de imagen y las 32 entradas de paleta antes y después de la pausa
en el estudio, los cuatro paneles, los actos musicales y las áreas de Daniel.


## Segundo episodio v0.12.0

`episode` distingue los dos capítulos. El estado MISSION (9) muestra una tarjeta
sin reloj al entrar o reintentar una misión del directo. A en el cierre del primer
episodio conserva puntuación y medallas, limpia los tres sellos actuales y abre
el segundo. Remix se desbloquea al cerrar ambos. Todo el progreso sigue en RAM;
el encabezado del cartucho no anuncia batería.

En Chucho, `link_mask` representa energía, cámara, mezcla y transmisión. Energía
abre cámara y mezcla; las dos abren memoria. El jugador puede invertir las dos
reparaciones intermedias. Hay tres enlaces de cuatro reparaciones. Comienzan con
99 segundos y cada enlace intermedio recupera hasta ocho segundos. Las averías
tienen 22 segundos de plazo exterior; si una vence, se pierde un corazón y su
plazo se reinicia en 18 segundos, conservando una salida posible para la cadena.
Todos los plazos siguen congelados en los paneles.

La rutina nueva pide 49 aciertos contando la práctica, con cambios de acto al
llegar a 17 y 33. Una nota entra cada 90 cuadros; cada cuarta nota tiene una cola
de 30 cuadros. Durante la sostenida, las demás notas y la música siguen avanzando.
Soltar antes produce un solo fallo. Tras una pausa, `hold_resume` conserva la
nota y la música hasta que el jugador retoma el botón correspondiente. Las tres
composiciones nuevas usan las pistas 8, 9 y 10.

Daniel usa dos objetos opcionales por mundo, ubicados en una franja que no tiene
personas. Sus posiciones y zonas se eligen una vez por mundo. `prop_mask` impide
recogerlos dos veces y se conserva al cambiar de distrito. Cada objeto añade
150 puntos y hasta diez segundos, con tope de 99; la pista indica el lado de la
plaza o el distrito de Daniel. No son condición para ganar ni para la medalla.
La página de sprites 46 también contiene sus ocho tiles y los dos tiles de cola
que utiliza la nueva rutina; el resto del arte original se conserva.

Los mapas originales y la ExRAM del título se movieron al banco PRG 1. El banco 0
mantiene los distritos, la intro y la tarjeta compartida. Los cargadores viven en
el banco fijo, trabajan con NMI y renderizado apagados y restauran el banco 12
antes de volver a C. `EXTRACODE` utiliza el espacio liberado del banco fijo para
las pantallas y las misiones nuevas. La ROM conserva 128 KiB PRG, 256 KiB CHR y
50 bancos gráficos ocupados. El HUD convierte sus cifras sin división de 16 bits
para mantener el ritmo dentro del presupuesto de un cuadro.

`second_episode_test.py` juega las dos campañas normal y Remix mediante controles.
Comprueba dependencias en ambos órdenes, fallos recuperables, sostenidas,
reanudación, música, objetos opcionales, visitas repetidas, reinicios y presupuesto
de sprites/cuadros. `second_episode_mesen.lua` recorre ambos episodios con su propio
controlador, verifica los textos de resultados y compara el fondo y la paleta de
los tres juegos antes y después de pausa y ayuda. No escriben RAM ni cargan estados.


## Entradas y controles v0.12.1

CHARACTER_INTRO (7) amplía la entrada a los tres personajes del primer episodio,
incluidos sus reintentos y la elección desde el estudio o la ayuda. Conserva
A/Start para confirmar, B para volver y la espera sin reloj. La segunda grabación
mantiene sus tarjetas de misión. Los nuevos pósteres usan CHR 50–53; sus mapas,
atributos y paletas ocupan PRG 2. El cargador fijo restaura PRG 12 antes de volver
a C. La intro original de Dany sigue usando PRG 0 y CHR 47/48.

La ayuda prepara siete filas en un búfer de 224 bytes. Una rutina 6502 centra el
texto sin exceder el tiempo de un cuadro. NMI publica solo las 26 columnas interiores
de cada fila, 182 bytes en total. En ese cuadro omite el DMA de OAM ya vacío: la
pantalla no tiene sprites que actualizar. Conserva los bordes, la paleta y la
imagen completa durante los cambios rápidos. Los controles inferiores están en
las filas 25 y 27, separados de la línea inferior del marco.

El generador de plazas despeja franjas laterales de 16 píxeles y franjas superior
e inferior de ocho. Las flechas forman parte del fondo y dependen de las conexiones
del distrito. No cambian posiciones de personas, objetos, límites del cursor ni
la selección por distancia. Los rótulos de tiendas quedan encima del borde superior.

Antes de crear una nota se cuenta el total de aciertos más notas activas. Si ya
alcanza el objetivo del acto, se espera a resolver esa cola. Fallar libera una plaza;
la nota de reemplazo conserva la cadencia musical. El último acierto vacía la pista,
también con sostenidas, sin cambiar las ventanas de pulsación ni los objetivos.

`usability_test.py` comprueba tarjetas, permanencia, salida, reintentos, reinicio,
cada imagen de cambios rápidos de ayuda, direcciones visibles y fallos de la última
nota en ambos episodios. `usability_mesen.lua` valida de forma independiente el
mapa cargado, las imágenes y los cuadros de ayuda. La campaña de Mesen comprueba
también que ningún acto cree notas sobrantes. Las pruebas usan únicamente controles.
