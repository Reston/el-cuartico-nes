# Desarrollo

## Cartucho y código

El juego usa un encabezado iNES, mapper **MMC5 (5)**, 128 KiB de PRG y 256 KiB de
CHR. Hay 49 bancos gráficos de 4 KiB ocupados. La memoria de batería no se utiliza.

- `src/game.c`: estados, entrada, campaña y minijuegos.
- `src/start.s`: arranque 6502, NMI, DMA de sprites y configuración MMC5.
- `src/music.h`: temas y efectos de la APU.
- `src/nes.cfg`: mapa de memoria de cc65.
- `assets/likeness.py`: personajes y poses mediante píxeles indexados.
- `assets/quality.py`: escenas, animaciones, tiles y atributos MMC5.
- `assets/generate.py`: punto de entrada para generar los recursos gráficos.

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

Primero compila con `./build.ps1`. `tools/test_all.py` ejecuta nueve suites de
FCEUmm; `--mesen` añade una campaña independiente con Mesen. Los resultados se
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
