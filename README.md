Este juego fue creado enteramente con IA para probar las capacidades de Astra.

<div align="center">

# El Cuartico: ¡Estamos grabando!

**Tres personajes. Tres juegos. Un episodio por publicar.**

<img src="docs/media/portada.png" alt="Portada ilustrada de El Cuartico: Estamos grabando" width="260">

**NES · MMC5 · Un jugador · v0.10.0**

[🎮 Descargar ROM](https://raw.githubusercontent.com/Reston/el-cuartico-nes/main/dist/el-cuartico-v0.10.0-mmc5.nes) · [Cómo jugar](#cómo-jugar) · [Compilar](#compilar-el-juego) · [Desarrollo](docs/DESARROLLO.md)

</div>

Un juego *homebrew* inspirado en **El Cuartico**, hecho para jugarse en emuladores
de NES. Elige a **Chucho, Estefania o Daniel** y completa sus desafíos en el orden
que quieras. Cada victoria deja un sello; consigue los tres para publicar el episodio.

## Edición episodio remix

Versión **v0.10.0** aprobada e integrada en `main`.
[Guía del episodio remix](docs/PRUEBA-REMIX.md).

- **Reacciones:** mensajes breves de los personajes y celebración al reparar.
- **Chucho:** apagón, acople y grabación en directo, en orden variable. Resolver
  la estación indicada da 200 puntos y recupera un corazón si te falta alguno.
- **Puzles:** más combinaciones de cables y objetivos de enfoque variables.
- **Estefania:** calentamiento, pasito y remate, con música y luces propias.
- **Daniel:** mercado, paseo musical, jardín, patio de arte y calle de flores,
  con caminos reflejados y puntos de referencia distintos.
- **Estudio compartido:** pulsa B en la selección, camina hasta un personaje y
  pulsa A. B vuelve al menú de retratos.
- **Medallas y final:** las tomas limpias conservan su medalla en el menú;
  tres medallas perfectas tienen un reconocimiento en el cierre. B anima la fiesta.
- **Remix:** después de ganar los tres juegos, A inicia otra campaña con más
  señuelos y variantes. Start comienza una campaña normal.

| El estudio compartido | Tres actos musicales | Fiesta del episodio |
| :---: | :---: | :---: |
| ![Estudio para elegir juego](docs/media/estudio.png) | ![Segundo acto](docs/media/acto-2.png) | ![Celebración final](docs/media/final.png) |

## Un vistazo al juego

| Elige tu personaje | Sigue el ritmo | Encuentra a Daniel |
| :---: | :---: | :---: |
| ![Selección de personajes](docs/media/personajes.png) | ![El sketch de Estefania](docs/media/estefania.png) | ![Una zona del barrio de Daniel](docs/media/daniel.png) |

| Conecta los cables | Atrapa la señal | Recuerda la secuencia |
| :---: | :---: | :---: |
| ![Reparación de cables](docs/media/cables.png) | ![Minijuego del mezclador](docs/media/mezcladora.png) | ![Reparación de la señal](docs/media/memoria.png) |

## Jugar ahora

1. Descarga [**el-cuartico-v0.10.0-mmc5.nes**](https://raw.githubusercontent.com/Reston/el-cuartico-nes/main/dist/el-cuartico-v0.10.0-mmc5.nes).
2. Ábrelo en un emulador con soporte **MMC5**, como FCEUmm o Mesen.
3. Usa el **control 1**, región **NTSC** y velocidad normal. No hace falta BIOS.

Al actualizar, inicia desde cero: los estados guardados de una ROM anterior no
son compatibles con esta versión. La música y los gráficos están dentro del archivo.

En [dist/](dist/) solo se conserva la entrega actual: la ROM, las instrucciones
breves y su [checksum SHA-256](dist/SHA256.txt).

### En R36S o Retroid

- **R36S con ArkOS:** apaga la consola, copia la ROM a la carpeta `nes` de la tarjeta
  de juegos, expulsa la tarjeta de forma segura y abre el juego en la lista de NES.
- **Retroid:** copia la ROM a tu carpeta de juegos y ábrela en RetroArch con el núcleo
  FCEUmm. Si no aparece al escanear, usa **Cargar contenido** y selecciona el archivo.
- Si A y B están intercambiados, ajusta el mapeo del control 1. Para el juego de ritmo,
  usa altavoces o auriculares con cable y desactiva la aceleración y el turbo.

La versión actual se prueba en FCEUmm y Mesen de escritorio. Una versión anterior
fue probada en R36S; la entrega actual todavía necesita validación en la consola.

## Cómo jugar

### Chucho · Mantén el estudio funcionando

Completa **12 reparaciones**, con **75 segundos iniciales** y **cinco corazones**.
Muévete por el estudio, acércate a una estación averiada y pulsa **A** para abrir
su minijuego. **B** permite correr cuando el indicador está listo.

| Estación | Reparación | Qué hacer |
| --- | --- | --- |
| Arriba a la izquierda | Cables | Usa arriba/abajo para elegir el terminal derecho y pulsa A para unir el número indicado. Completa tres conexiones. |
| Arriba a la derecha | Enfoque | Mueve la estrella con izquierda/derecha hasta el recuadro y confirma con A. Ajusta dos objetivos. |
| Abajo a la izquierda | Atrapa la señal | Pulsa A cuando la estrella pase por el recuadro. Necesitas tres aciertos; el objetivo cambia de posición después de cada uno. |
| Abajo a la derecha | Memoria | Observa cuatro direcciones y repítelas con la cruceta. Cada flecha se muestra durante un segundo, con pausas entre ellas. |

**B cierra el panel** sin reparar la estación. Los errores tienen respuesta visual,
pero no quitan corazones. Dentro de los minijuegos aparece **SIN LÍMITE**: tanto
el reloj del episodio como los plazos de las otras averías quedan congelados.
Tómate el tiempo que necesites; el reloj solo corre cuando vuelves al estudio.

Después de las reparaciones 3, 6 y 9 aparece un evento. Atiende la estación
indicada en la franja superior para conseguir su premio; los eventos mantienen
la pausa del reloj dentro del panel. El apagón cambia la luz del estudio y el
acople desafina el monitor hasta que reparas los cables.

Cada cuarta reparación añade **tres segundos**. Encadenar reparaciones aumenta el
multiplicador de puntos. Dejar vencer una avería en el estudio cuesta un corazón.

### Estefania · El sketch

Pulsa **A, B o la dirección indicada** cuando el símbolo llegue al recuadro.
La primera A es una práctica sin tiempo; después hay una cuenta de cuatro tiempos.
Consigue **20 aciertos** antes de acumular cinco fallos. Al alcanzar 7 y 13 aciertos
cambian la música, las luces y el patrón de notas. Cada acto vuelve a contar cuatro
tiempos: ninguna nota pendiente se cobra como fallo durante el cambio.

Los aciertos precisos dan puntos extra, y cada cinco aciertos consecutivos de la
secuencia añaden otros 100 puntos. La música y las notas se detienen juntas al pausar.

### Daniel · ¿Dónde está Daniel?

Explora la plaza y compara las caras con el retrato de referencia. Hay un solo
Daniel en cada mundo, y las personas mantienen su posición cuando vuelves a una zona.

| Búsqueda | Tamaño del mundo | Personas | Tiempo inicial |
| --- | --- | --- | --- |
| Plaza | Una zona | 12 | 60 segundos |
| Mercado | Dos zonas contiguas | 32 | 85 segundos |
| Barrio | Cuatro zonas, en una cuadrícula de 2 × 2 | 80 | 99 segundos |

- **Cruceta:** mueve el cursor. Cruza el borde indicado en la franja **CRUZA** para
  pasar a otra zona; el mapa pequeño marca dónde estás y qué zonas visitaste.
- **Mantener B:** abre la lupa sobre una persona y permite moverte con precisión.
  Suelta B para cruzar a otra zona.
- **A:** elige a la persona enfocada. Equivocarte cuesta **cinco segundos**.

Las salidas aparecen debajo de la plaza, sin tapar personas. Los pájaros se ocultan
al usar la lupa. Encuentra a Daniel una vez en cada mundo para conseguir su sello.

### Pausa y progreso

| Situación | Controles |
| --- | --- |
| Selección | Izquierda/derecha o Select para elegir; A o Start para empezar. |
| Durante un juego | Start pausa. |
| En pausa | Start continúa, A reinicia el intento y B vuelve a la selección. |
| Estudio compartido | Cruceta para caminar, A junto a un personaje, B para volver al menú. |
| Final del episodio | B anima la fiesta, A comienza Remix y Start una campaña normal. |

Los sellos de victoria duran la sesión actual y se conservan al reintentar otro
juego. Las medallas son opcionales: tres por una partida sin errores; dos si no
superas dos fallos ni dos errores de reparación; una por las demás victorias.
Equivocarte dentro de un panel no quita corazones, pero cuenta para esa medalla.

En **Remix**, el enfoque pide tres confirmaciones y la mezcladora cuatro aciertos.
Estefania usa otras combinaciones de botones, y Daniel tiene 16, 40 y 96 personas
repartidas entre uno, dos y cuatro lugares. Se conservan los tiempos normales,
la velocidad pausada de memoria y los paneles sin límite.

No hay guardado por batería. Usa estados del emulador únicamente con la
misma versión de la ROM y el mismo núcleo.

## Compilar el juego

La ruta de desarrollo preparada es **Windows + PowerShell**, con Python 3.10 o
superior, Pillow y cc65. El script de instalación descarga las herramientas en
`tools/`; esos binarios no se incluyen en Git.

```powershell
git clone https://github.com/Reston/el-cuartico-nes.git
cd el-cuartico-nes
python -m pip install -r requirements.txt
python tools/bootstrap.py
./build.ps1
python tools/package.py
```

La compilación genera `build/el-cuartico.nes`. El empaquetador copia esa ROM a
`dist/` con la versión de [VERSION](VERSION) y actualiza `SHA256.txt`.

### Ejecutar las pruebas

```powershell
python tools/bootstrap.py --test-tools
./build.ps1
python tools/test_all.py --mesen
```

Las pruebas usan entradas de control en FCEUmm y una campaña independiente en Mesen.
Comprueban los seis órdenes de juego, victorias y derrotas, pausa, ritmo, selección,
los cuatro paneles de reparación, navegación, límites de sprites y tiempos de cuadro.
Los informes, capturas y grabaciones se guardan en `build/`, fuera del control de versiones.

## Estructura del proyecto

```text
src/              Código C, arranque 6502, música y configuración del cartucho
assets/           Arte nativo por tiles, generadores y gráficos del juego
tools/           Compilación auxiliar, emuladores de prueba y validación
docs/            Documentación y capturas para este repositorio
dist/            Solo la última ROM, instrucciones y checksum
build/           Resultados locales de compilación y pruebas; ignorados por Git
```

Los intentos anteriores y los materiales de trabajo se archivan **fuera del
repositorio**. No forman parte de `dist/` ni de la descarga del código.

## Créditos y licencia

Proyecto fan no oficial inspirado en **El Cuartico** y sus personajes. El arte de
los personajes toma como referencia las fotografías compartidas durante el desarrollo.
El juego incluye gráficos por tiles y música para la APU de NES.

Herramientas: [cc65](https://github.com/cc65/cc65),
[FCEUmm](https://github.com/libretro/libretro-fceumm),
[Mesen CE](https://github.com/nesdev-org/MesenCE) y
[Pillow](https://github.com/python-pillow/Pillow).

Se conserva la licencia **GNU GPL v3** del repositorio. Consulta [LICENSE](LICENSE).
