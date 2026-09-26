# Plan de aventura: El Cuartico — Una última toma

**Estado:** propuesta de diseño y producción; ninguna de estas funciones nuevas está implementada.
**Fecha:** 26 de septiembre de 2026. **Base:** juego v0.13.1.
**Plataforma:** NES, un jugador, mando de dos botones; R36S como dispositivo principal de prueba portátil.

## 1. La idea que une el juego

Chucho, Estefania y Daniel quieren grabar un sketch. Tienen el estudio, los equipos
y demasiadas ideas. Cada propuesta se convierte en una aventura que imaginan y
ensayan juntos. Al terminar conservan una parte que funciona: la premisa, el
conflicto o el remate. El final consiste en grabar una versión que une esas partes.

**Promesa para quien juega:** ayudar al Cuartico a convertir una idea absurda en
un sketch terminado, jugando sus ensayos como una aventura de plataformas y acción.

El estudio es real dentro de la historia; los mundos son representaciones de sus
ideas. Una claqueta y un cambio visual distinguen ambas situaciones. Las derrotas
son tomas fallidas, no muertes de los personajes. La urgencia de grabar forma parte
del diálogo: no existe una cuenta atrás global que obligue a apresurarse.

### Decisiones de partida

- Un motor compartido de plataformas laterales, con combate sencillo y exploración.
- Tres ensayos principales de dos fases cada uno, más una grabación final.
- Tres personajes jugables; cambio en puntos seguros, no durante un salto.
- Los juegos actuales pasan a ser tareas de producción y siguen disponibles completos.
- Progreso recuperable mediante contraseña; terminar la historia no exige medallas.
- Gráficos, música, personajes secundarios y mapas originales. Las referencias a
  otros juegos orientan el diseño y la comedia; no son una lista obligatoria de diez títulos.

El título, los diálogos, los nombres de jefes y las cifras de equilibrio son
propuestas editables. La estructura narrativa anterior guía el desarrollo.

## 2. Reglas de diseño

1. **Todo objetivo tiene un motivo en el sketch.** Se cruza una azotea para entregar
   un paquete; se combate una máquina porque retiene la dirección del destinatario.
2. **Moverse debe ser divertido antes de añadir contenido.** Saltos, cámara,
   colisiones y respuesta del ataque se prueban primero con gráficos simples.
3. **La comedia se juega.** Un portero pide un permiso para entregar el permiso;
   una máquina interpreta una instrucción literalmente. El diálogo prepara el gag.
4. **Cada ensayo deja algo útil.** El guion visible en el estudio avanza y el final
   recupera sus hallazgos. Ningún mundo termina siendo una excursión sin consecuencia.
5. **La variedad conserva controles y reglas aprendidas.** Cambian situaciones,
   enemigos y ritmo; no se construye un motor nuevo para cada homenaje.
6. **Los errores invitan a otra toma.** Reintentos cortos, puntos de control y ayuda
   opcional. Los chistes de derrota se pueden saltar y no se repiten siempre.
7. **Legibilidad en portátil.** Texto breve, objetivo reconocible, peligros claros
   y efectos que no oculten las plataformas ni los ataques enemigos.

## 3. Historia y progresión

### Premisa del sketch: «Entrega sin interrupciones»

Un repartidor debe entregar una caja a un estudio sin interrumpir la grabación.
El recorrido se vuelve más ruidoso y complicado cuanto más intenta ayudar todo
el mundo. Dentro de la caja hay un cartel: **SILENCIO. ESTAMOS GRABANDO.**

El remate llega cuando por fin cuelgan el cartel, se hace silencio y suena el
timbre de otra entrega. El jugador da la última respuesta: abrir la puerta.
Es una propuesta de gag final, no una cita ni una recreación de un sketch existente.

| Momento | Qué sucede | Qué aporta al guion |
| --- | --- | --- |
| Prólogo | Los tres acuerdan empezar con una entrega sencilla. Se aprende a moverse en un decorado de ensayo. | Una caja y una misión comprensible. |
| Ensayo 1: La entrega imposible | Daniel propone que hasta llegar a la puerta sea una aventura. Estefania añade un portero demasiado importante. | La ruta del repartidor y el chiste del permiso. |
| Ensayo 2: La casa que ayuda demasiado | Chucho propone automatizar la entrega. Todos los aparatos interpretan mal sus instrucciones. | El conflicto: cada solución hace más ruido. |
| Ensayo 3: ¿Quién pidió esto? | Nadie reconoce al destinatario. Buscan pistas mientras una voz exige silencio desde una cabina. | El destinatario y el remate de la caja. |
| Preparación final | Ordenan el guion, comprueban las tareas de producción y eligen al protagonista de la toma. | Premisa, conflicto y remate completos. |
| Grabación | Una ruta nueva mezcla los mejores obstáculos, con montaje más rápido y un último problema. | El sketch terminado. |
| Epílogo | Ven una breve versión editada, reaccionan y desbloquean la selección de tomas. | Recompensa y motivos para volver. |

### Un ejemplo del tono

> Chucho: «Llega, entrega la caja y se va».
>
> Daniel: «¿Y si la casa no tiene puerta?»
>
> Estefania: «Tiene. Pero el portero es el jefe final».
>
> Chucho: «Todavía no hemos grabado ni el timbre».

Estas líneas sirven de referencia de ritmo. La voz definitiva de los personajes
se revisa antes de producir todas las escenas; no se inventan citas reales.

### Gramática de una misión

Propuesta breve en el estudio → objetivo visible → ensayo jugable → una reescritura
en un lugar seguro → prueba de lo aprendido → remate → pieza de guion obtenida.

Una reescritura cambia la siguiente sala o tramo, nunca el suelo bajo el jugador
sin aviso. No anula coleccionables ni obliga a repetir una fase terminada.
Como máximo hay una interrupción narrativa obligatoria por fase, además de entrada
y cierre. Las escenas se avanzan manualmente; tras el primer intento se pueden omitir.

## 4. Campaña y mundos

La campaña inicial tiene orden fijo para poder construir el chiste y la dificultad.
Después de completar una fase se permite repetirla desde la mesa de guion.
Cada ensayo contiene dos fases; el enfrentamiento principal está dentro de la segunda.

### Ensayo 1 — La entrega imposible

**Referencia de diseño:** claridad de rutas y saltos de Mario; decorados y enemigos propios.

- **Fase 1, Calle de cartón:** plataformas anchas, toldos elásticos y dos tipos de
  obstáculo. Enseña salto variable, ataque, interacción y punto de control. Una
  flecha exagerada conduce a un desvío que vuelve a la misma puerta: primer gag jugable.
- **Fase 2, Azoteas y recepción:** plataformas móviles y una ruta alternativa visible.
  La reescritura «la entrada está arriba» convierte el acceso al edificio en un ascenso
  por salas conectadas, sin exigir cámara vertical continua.
- **Jefe, El Portero de Utilería:** golpea con su sello, desliza una barrera y descansa
  revisando papeles. Se esquiva el patrón y se ataca durante la revisión. No exige reflejar
  proyectiles ni dominar una habilidad que todavía no se ha enseñado.
- **Pieza conservada:** el permiso inútil, que vuelve como llave cómica en el final.
- **Tarea de producción:** Chucho repara el mecanismo de una puerta del decorado.

### Ensayo 2 — La casa que ayuda demasiado

**Referencia de diseño:** patrones legibles y salas de acción de Mega Man.

- **Fase 3, Recepción automática:** cintas transportadoras, sensores y pequeños
  aparatos que intentan clasificar la caja. Primero se presenta cada peligro por separado.
- **Fase 4, Central del buen servicio:** combina un peligro de recorrido con enemigos
  a distancia. La reescritura «que la casa ayude» activa máquinas que dificultan el camino.
- **Jefe, La Asistente Perfecta:** alterna aspirar, expulsar paquetes y anunciar una
  solución equivocada. Luces y animación anticipan cada acción. Vencerla entrega la
  etiqueta correcta; no añade un inventario de armas.
- **Pieza conservada:** una instrucción que siempre se interpreta al revés.
- **Tarea de producción:** Estefania ensaya una cortinilla para cubrir un cambio de escena.

### Ensayo 3 — ¿Quién pidió esto?

**Referencia de diseño:** pistas y descubrimientos de Zelda, con ambientación de
estudio nocturno; se mantiene la vista lateral y el mismo motor.

- **Fase 5, Camerinos equivocados:** un pequeño circuito de salas, tres pistas claras
  y personajes que confunden al repartidor. Un esquema de salas ayuda a orientarse.
- **Fase 6, Cabina de silencio:** combina exploración y plataformas. Las pistas revelan
  que el misterioso destinatario está en el propio estudio. No hay objetos obligatorios
  ocultos sin indicación ni combinaciones arbitrarias de inventario.
- **Jefe, El Director del Silencio:** produce ruido cada vez que ordena callar; sus
  focos y altavoces anticipan las zonas peligrosas. Tras el combate pide el cartel de la caja.
- **Pieza conservada:** la contradicción que da sentido al remate.
- **Tarea de producción:** localizar a Daniel entre los figurantes antes de grabar
  su intervención. Se conserva así la lógica del juego de búsqueda actual.

### Final — Ahora sí, grabando

Un montaje jugable de tres tramos breves utiliza el permiso, la casa automática
y la cabina. Son disposiciones nuevas de mecánicas conocidas, no una repetición
íntegra de las seis fases. Hay un punto de control entre tramos.

El último enfrentamiento combina dos patrones ya aprendidos y termina al entregar
la caja, no al descubrir un cuarto sistema de combate. Sigue la acción breve de
colgar el cartel y abrir la puerta tras el timbre. El epílogo muestra a los tres.

La caja es un objeto de historia: aparece con el personaje o en la escena, pero no
añade física de transporte, durabilidad ni pérdida permanente. Todos los protagonistas
pueden completar la entrega. Las tareas de producción pendientes pueden hacerse
antes de empezar la toma final; no interrumpen el clímax.

## 5. Personajes y controles

Los tres comparten salto, velocidad base, salud, invulnerabilidad tras un golpe
y capacidad de completar el recorrido principal. Sus animaciones y oportunidades
especiales expresan personalidad sin crear tres campañas diferentes.

| Personaje | Ataque con B | Interacción característica | Recompensa opcional |
| --- | --- | --- | --- |
| Chucho | Golpe corto con herramienta de utilería. | Activar un mecanismo señalado. | Plataforma que abre un atajo. |
| Estefania | Pulso de sonido corto, con recuperación visible. | Activar un interruptor de resonancia. | Ruta alternativa hacia una cinta. |
| Daniel | Destello corto de la lupa; misma función básica de combate. | Inspeccionar una marca para revelar una pista. | Identificar una pared falsa o el camino más corto. |

Los alcances y tiempos se equilibran con pruebas, sin anunciar uno como superior.
Las oportunidades especiales se indican antes de elegir personaje en el punto
seguro. Ninguna bloquea una salida obligatoria. Los tres hablan durante la historia
aunque solo uno esté representado físicamente en el tramo.

| Contexto de aventura | Acción |
| --- | --- |
| Izquierda / derecha | Caminar. Sin botón de carrera obligatorio. |
| A | Saltar; mantener permite un salto más alto dentro del límite definido. |
| B | Ataque del personaje. |
| Arriba, junto a un indicador | Hablar, usar un mecanismo o abrir una puerta. |
| Arriba, junto al camerino | Abrir selección de personaje; A confirma y B vuelve. |
| Start | Pausar o continuar. |
| Select en pausa | Consultar controles, conservando la convención actual. |

No se añaden acciones indispensables con combinaciones ocultas de botones. Abajo
y Select durante la acción quedan libres en la primera versión. Los minijuegos
conservan sus controles; cada entrada muestra claramente el cambio de actividad.

**Punto inicial para ajustar movimiento:** tolerancia al salto al abandonar un borde
y pulsación anticipada de unos pocos cuadros, daño con invulnerabilidad breve y
retroceso limitado. Sus valores se fijan jugando, no solo mirando una animación.
No se añade escalada, agarre de bordes, pendientes ni combate con combos al primer motor.

## 6. Los minijuegos existentes dentro de la historia

Se reutilizan las reglas y recursos actuales mediante variantes cortas. Estas
variantes tienen objetivos propios y no cambian la dificultad del modo original.

| Actividad | Versión de historia propuesta | Duración objetivo | Resultado narrativo |
| --- | --- | --- | --- |
| Chucho: reparar | Dos paneles de reparación; sin reloj mientras se resuelven. | 30–60 segundos. | La puerta del decorado funciona. |
| Estefania: ritmo | Práctica breve y una frase de 8–12 notas; cierre en un límite musical. | 20–40 segundos. | Cortinilla ensayada. |
| Daniel: búsqueda | Una zona de público y una búsqueda, con pista progresiva. | 30–60 segundos. | Actor localizado para su escena. |

Estas cifras son metas de adaptación, no mediciones del juego actual. La música
y el número de notas deben diseñarse juntos; no se recorta el sonido de forma abrupta.

- Se presentan una vez cada una en la ruta principal, separadas entre ensayos.
- Tras dos intentos fallidos se ofrece ayuda o «el equipo termina la preparación».
  Ayudar permite continuar y mantiene disponibles todos los finales narrativos.
- Un fallo no reinicia la fase de plataformas ni reduce la salud del aventurero.
- La entrada guarda el identificador de retorno y el progreso permanente. La salida
  reconstruye la sala en un punto seguro; no intenta guardar toda la simulación.
- Su éxito o ayuda marca una tarea de producción. No entrega sellos de los episodios
  clásicos ni modifica sus puntuaciones por accidente.
- Una estación del estudio ofrece los dos episodios y Remix actuales completos,
  bajo **Juegos del estudio**. Se conservan también como acceso directo del menú.

El menú principal propuesto: **Aventura**, **Contraseña**, **Juegos del estudio**
y **Cómo jugar**. No se obliga a repetir los seis juegos anteriores para acceder
a la aventura o a sus personajes.

## 7. Estudio, recompensas y duración

El estudio actual es la base visual y espacial. Se añaden tres puntos claros:
la mesa del guion, el camerino y el monitor de juegos. El guion muestra tres casillas:
**inicio**, **problema** y **remate**. Cada ensayo completa una y añade un accesorio
visible al decorado. Así el progreso se entiende sin una explicación extensa.

### Alcance de la primera campaña completa

| Contenido | Cantidad prevista |
| --- | --- |
| Estudio y prólogo interactivo | 1 conjunto compartido. |
| Ensayos | 3, con identidad visual y mecánica propia. |
| Fases principales | 6, aproximadamente 4–7 minutos cada una, jefe incluido cuando corresponda. |
| Jefes de ensayo | 3; el final reutiliza y combina comportamientos. |
| Minijuegos narrativos | 3 adaptaciones cortas de los existentes. |
| Grabación final | 1 secuencia de tres tramos, objetivo de 8–12 minutos. |
| Cintas opcionales | 6, una por fase; cada una desbloquea un gag o variante visual. |
| Familias básicas de enemigos | 6: dos introducidas por ensayo, con reutilización posterior. |

**Objetivo de duración:** 45–75 minutos en una primera partida, contando escenas,
exploración y reintentos moderados. Las fases repetidas y el contenido opcional pueden
ampliarla. Es una hipótesis que se mide con personas nuevas; no una duración prometida.

Las cintas se conservan al morir o salir de una fase. Hay una ruta de recogida con
cualquier personaje; las especialidades ofrecen atajos. Conseguir las seis cambia
un detalle del epílogo y desbloquea una toma extra breve, construida con recursos
existentes. El final normal siempre contiene el sketch completo.

Las medallas de aventura reconocen terminar una fase y superarla sin recibir daño;
no otorgan mejoras de fuerza ni obligan a acumular puntos. Las medallas de los juegos
originales mantienen sus reglas. Remix de aventura, contrarreloj y una campaña
ramificada quedan para una ampliación posterior, no para esta entrega.

## 8. Dificultad, reintentos y recuperación de progreso

- Salud inicial propuesta: cuatro golpes; modo **Ensayo tranquilo** reduce daño
  y amplía la tolerancia de los retos narrativos. **Toma normal** es la referencia de equilibrio.
- No hay vidas limitadas. Un golpe fatal o una caída devuelve al último punto seguro.
- Punto de control aproximadamente cada 60–90 segundos y antes de cada jefe.
  Tras morir se restauran salud y enemigos del tramo, conservando premios permanentes.
- El jugador puede activar ayuda desde pausa sin reiniciar la campaña. No hay un
  final peor por hacerlo. Las medallas de reto indican las condiciones de la toma.
- Se pueden repetir jefes y fases terminadas desde el guion; no se pierde progreso
  de historia por entrar a practicar.

### Contraseña

La primera versión guarda progreso de aventura mediante un código visible y fácil
de fotografiar en el R36S. No depende de batería ni de estados del emulador.

Formato de trabajo: **12 símbolos en tres grupos de cuatro**, con un alfabeto de
32 caracteres que evite letras y números confundibles. Presupuesto inicial de 60 bits:
versión de formato (4), fases completadas (6), ensayos cerrados (3), tareas de producción
(3), cintas (6), medallas (12), final completado (1), dificultad (1), reservado (8)
y comprobación de errores (16). La codificación definitiva se revisa en el hito de progreso.

La contraseña recupera el estudio y sus desbloqueos. **No** conserva el punto exacto
dentro de una fase, salud, puntuaciones temporales ni partidas de los juegos clásicos.
Se muestra al volver al estudio y en pausa junto al aviso de que restaura desde el
estudio. Si se sale a mitad de una fase, esa fase vuelve a comenzar.

La carga valida formato, comprobación e invariantes narrativas antes de tocar la
partida activa. Un código incorrecto muestra una explicación breve y permite editarlo.
No se interpreta una contraseña de otra versión silenciosamente. Si la historia
cambia, se conserva el decodificador o se comunica la incompatibilidad explícitamente.

## 9. Presentación, arte y sonido

### Lectura y comedia

- HUD mínimo: salud e icono del objetivo; el nombre y la explicación completa van en pausa.
- Objetivos cortos: «ENTREGA LA CAJA», «RECUPERA LA ETIQUETA», «BUSCA LA CABINA».
- Diálogos con retrato, como máximo dos líneas cortas por tarjeta y avance manual.
  El generador valida el ancho en píxeles, no solo el número de caracteres.
- Área útil con margen: evitar texto crítico junto al borde inferior, ya problemático
  en la versión anterior. Comprobar cada pantalla en la resolución nativa y en R36S.
- Peligros reconocibles por silueta y animación, además del color. El juego de ritmo
  sigue dando información visual suficiente para jugar sin depender del sonido.
- Reescrituras, éxito y fracaso comparten la claqueta. Evitar sacudidas grandes o
  destellos repetidos; cualquier efecto de impacto debe permitir ver la próxima acción.

### Producción de recursos

Primero, un juego de tiles y un personaje con poses de reposo, carrera, salto,
ataque, daño e interacción. Después de validar movimiento, completar los otros dos,
tres familias de escenarios, seis familias de enemigos y tres jefes.

Compartir formas de colisión y animaciones cuando ayude, pero distinguir los ensayos
con composición, accesorios y ritmo de juego. Los homenajes no usan sprites, mapas,
logos, melodías ni personajes extraídos de Mario, Mega Man u otros juegos.

El menú y el minijuego de Estefania conservan sus arreglos actuales. La aventura añade
motivos originales por ensayo, transiciones breves y una versión final que reúna esos
motivos. El canal reservado a efectos debe seguir disponible durante ataques y saltos.
Pausa, cambio de sala y retorno de un minijuego restauran música y efectos correctamente.

**Restricción vigente del usuario:** no añadir grabaciones originales, canciones,
archivos de audio de referencia ni previsualizaciones renderizadas a la base de código
o a los PR. Mantener las partituras y datos sintetizados necesarios para que la ROM
suene, como en la implementación actual. Las pruebas de audio procesan PCM en memoria.

## 10. Base técnica y riesgos concretos

Fuentes locales revisadas: [arquitectura actual](DESARROLLO.md),
[mapa del enlazador](../src/nes.cfg), [arranque y NMI](../src/start.s),
[estados actuales](../src/game.c) y [pruebas](../tools/test_all.py).

### Lo que existe y lo que falta

Existe un cartucho MMC5 de 128 KiB PRG y 256 KiB CHR, selección de personajes,
estudio, juegos, música, retratos, pausa y suites en FCEUmm/Mesen. No existe todavía
el motor de plataformas, cámara desplazable, colisión con escenarios ni enemigos
de acción que necesita esta propuesta.

El artefacto local `build/el-cuartico.map` inspeccionado muestra 748 bytes de BSS
sobre una región configurada de 1024, unos 472 bytes libres al final de la ventana
CODE/RODATA y unos 2210 antes de vectores en el banco fijo. Son cifras de ese artefacto,
no una nueva compilación de esta propuesta. Deben repetirse y fecharse al iniciar P0;
tampoco contabilizan como libres las pilas o la memoria reservada a sprites.

`src/nes.cfg` tiene 72 KiB de relleno en EXPANSION. Es una oportunidad para mapear
código/datos nuevos, no espacio ejecutable que el compilador use automáticamente.
La documentación cuenta 54 bancos gráficos usados de 64; hay que inventariar índices
y contenido antes de comprometer recursos. No se presupone ampliar el cartucho.

### Arquitectura propuesta

Separar conceptualmente cuatro partes, sin reescribir el juego entero al comenzar:

1. **Estado persistente de aventura:** desbloqueos, guion, tareas, cintas y contraseña.
2. **Simulación de fase:** jugador, enemigos de capacidad fija, cámara, colisiones y punto seguro.
3. **Presentación:** tiles, cola acotada de VRAM, sprites, HUD, diálogo y transiciones.
4. **Puente de actividades:** entrada y retorno a REPAIR, RHYTHM y SEARCH con parámetros
   narrativos, sin confundirlos con la progresión clásica.

Ubicaciones de trabajo propuestas: `src/adventure/` para lógica,
`assets/adventure/` para datos y generación, y suites dedicadas en `tools/`.
La separación real en unidades compiladas y bancos se decide después del mapa de P0.
Las rutinas que cambian bancos y retornan a C necesitan una convención explícita
de llamada, restauración y acceso desde NMI; copiar el cargador de imágenes no basta.

**Modelo de niveles:** metatiles de 16 × 16, colisión sencilla, entidades declaradas
por sala y disparadores identificables. Probar desplazamiento horizontal con dos
nametables y transiciones de sala para cambios verticales. Sin mapa completo en RAM,
sin asignación dinámica y con límites explícitos para objetos y proyectiles.

**NMI y cámara:** la NMI actual restaura scroll a cero. El motor nuevo debe manejar
scroll, mirroring, carga de columnas y atributos con un presupuesto medido de vblank.
Prototipar HUD fijo frente a HUD integrado antes de elegir: no incorporar de entrada
un nuevo sistema de interrupciones por línea sin demostrar que hace falta.

**Pausa y ExRAM:** la pausa actual guarda una nametable completa en ExRAM. Una pantalla
desplazable puede depender de dos y de datos adicionales. Para aventura, preferir
una pausa que no destruya el escenario, o reconstruir ambas nametables desde el estado
de la sala con renderizado apagado. Validar entidades, paleta, cámara y audio al volver;
conservar el comportamiento actual para los juegos clásicos.

**RAM:** compartir buffers entre modos mutuamente excluyentes solo con ciclo de vida
documentado. Nunca solapar datos que pausa, NMI o retorno de minijuego todavía necesitan.
Antes de fijar el número de entidades, medir BSS, pila de C y pila de CPU con margen.

**Sprites y tiempo de cuadro:** diseñar encuentros alrededor de la capacidad medida.
Empezar con dos enemigos activos y un proyectil; ampliar solo tras probar escenas
exigentes. Priorizar jugador y peligros; reducir partículas y decorado primero.
No usar parpadeo del protagonista como solución permanente al exceso de sprites.

### Decisiones que se cierran con el prototipo

| Riesgo | Prueba necesaria | Alternativa si no alcanza |
| --- | --- | --- |
| Código actual casi llena su ventana | Compilar un módulo de aventura en banco separado y regresar sin corrupción. | Reorganizar bancos existentes antes de añadir contenido; ampliar PRG solo con decisión documentada. |
| Scroll, HUD y pausa compiten por recursos | Desplazarse, pausar en un borde de cámara y volver en ambos emuladores. | Salas de pantalla fija conectadas; elegirlo antes de diseñar las seis fases. |
| Demasiados gráficos únicos | Inventario CHR y prueba de un conjunto completo. | Compartir tiles, reducir poses decorativas o cambiar bancos entre salas. |
| Demasiados enemigos simultáneos | Escena de máxima carga con daño, disparos y música. | Menos enemigos con patrones mejores, sin quitar respuesta al control. |
| Integración altera los juegos actuales | Ir y volver de cada actividad y completar campaña clásica. | Adaptador separado, sin modificar su lógica de premios. |
| Duración conseguida mediante repetición | Sesiones de jugadores nuevos y registro de tiempos. | Recortar tramos repetidos y añadir una situación nueva por fase. |

## 11. Plan de construcción y entregables

Cada hito produce algo revisable. Los PR deben tener un objetivo claro; una fase no
se declara terminada por compilar. Las estimaciones de calendario se hacen después
de P2, cuando se conozca el coste real de motor, arte y una fase completa.

| Hito | Trabajo y entregable | Criterio para avanzar |
| --- | --- | --- |
| **P0 — Viabilidad** | Compilar base limpia, ejecutar regresiones, inventariar PRG/CHR/RAM, probar llamada a banco y resolver propuesta de scroll/pausa. Informe de presupuesto. | Hay un camino medido para una sala de aventura sin romper menú ni juegos. |
| **P1 — Movimiento** | Sala gris con Chucho, salto, cámara, plataformas, ataque, daño, caída, pausa y punto de control. ROM interna. | Movimiento legible y consistente en FCEUmm, Mesen y una prueba real en R36S; sin bloqueos ni fallos al pausar. |
| **P2 — Una toma completa** | Primera fase de 5–8 minutos con propuesta, dos enemigos, puerta/reparación corta, reescritura, jefe reducido y regreso al guion. Arte y sonido suficientes para juzgarla. | Un jugador nuevo entiende qué busca, identifica el chiste y quiere intentar otra fase. Se mide duración y se registra su confusión. |
| **P3 — Progreso y equipo** | Estructura de campaña, tres personajes, cambio seguro, contraseña, modo tranquilo, premios y acceso a juegos originales. | Guardar/cargar reconstruye desbloqueos, nadie queda sin salida y la campaña clásica sigue pasando sus pruebas. |
| **P4 — Ensayos completos** | Completar seis fases, tres jefes, otras dos tareas de producción y guion. Entregar por ensayo en PR separados. | Cada mundo enseña, desarrolla y combina una mecánica; todos los personajes completan la ruta principal. |
| **P5 — Grabación y epílogo** | Final de tres tramos, remate interactivo, devolución de los gags, cintas y selección de tomas. | Se puede terminar de principio a fin, también usando ayuda y contraseñas. La historia explica por qué se jugó cada ensayo. |
| **P6 — Equilibrio y entrega** | Pruebas externas, lectura portátil, rendimiento, revisión de audio, documentación y paquete. | Criterios de publicación cumplidos y recorrido físico en R36S registrado. |

Dependencia principal: **P0 → P1 → P2 → P3 → P4 → P5 → P6**.
Los bocetos narrativos pueden prepararse antes, pero la producción masiva de arte y
mapas espera a P2. Si el desplazamiento no convence, se ajusta P1; no se intenta
compensar con más mundos. El pequeño jefe de P2 se convierte en el jefe del primer
ensayo; no constituye contenido adicional que haya que mantener.

### Desglose inicial de PR

1. Presupuestos, puntos de entrada entre bancos y soporte mínimo de aventura.
2. Movimiento, colisiones, cámara y pruebas de pausa.
3. Ataque, enemigos, daño y puntos de control.
4. Primera toma completa y adaptador de reparación narrativa.
5. Campaña, menú, personajes, contraseña y aislamiento de progreso clásico.
6. Ensayo 1 definitivo, arte y primer jefe.
7. Ensayo 2 y adaptación narrativa del ritmo.
8. Ensayo 3 y adaptación narrativa de búsqueda.
9. Grabación final, epílogo y recompensas opcionales.
10. Equilibrio, comprobación portátil y versión pública.

Cada PR incluye alcance, instrucciones para probarlo, capturas cuando la imagen
importe, presupuesto actualizado si cambia bancos/memoria y resultados reales.
La integración continua puede usar una entrada de desarrollo para las fases
inacabadas; el menú público no anuncia contenido que todavía no se puede terminar.

## 12. Validación y definición de terminado

### Movimiento y combate

- Saltar desde bordes, aterrizar junto a paredes y golpear desde ambos lados sin
  atravesar sólidos ni quedar atrapado. Cámara estable al invertir dirección.
- Daño repetido, caída durante invulnerabilidad, muerte junto a salida y reintento
  reconstruyen un estado válido. Ningún jefe requiere un personaje concreto.
- Telegrafía visible antes del daño, espacio para reaccionar y recuperación clara.
- Presupuesto de cuadro comprobado en una escena exigente; registrar máximos,
  no solo promedios, y eliminar ralentizaciones que cambien el control.

### Estado, progreso y pausas

- Pausar durante salto, ataque, desplazamiento, diálogo y entrada/salida de actividad;
  consultar ayuda y volver sin alterar posición, cámara, enemigos o música.
- Probar retorno de cada minijuego con éxito, fallo, ayuda y abandono.
- Contraseñas: ida y vuelta de estados válidos, caracteres erróneos, comprobación
  incorrecta, versión desconocida y combinaciones imposibles. La carga fallida no
  cambia la partida activa. Se verifica también un reinicio real del emulador.
- Recoger una cinta, morir, salir, recargar y repetir no duplica premios ni los pierde.
- Juegos clásicos: dos episodios, Remix, música y pies de menú siguen funcionando.

### Historia, diversión y portátil

Probar con al menos tres personas que no conozcan los mapas, si están disponibles,
y preguntar qué intentaban hacer, qué parte conservaron del ensayo y qué les hizo
reír. Registrar tiempo por fase, muertes, abandonos, uso de ayuda y momentos de duda.
El criterio de P2 no se sustituye por una prueba automatizada.

En R36S comprobar salto y ataque con sus botones reales, lectura de diálogo y
contraseña, bordes de pantalla, sonido, reintento, pausa y una partida completa.
Los resultados en emuladores de escritorio se reportan por separado; si falta la
prueba física, queda pendiente y no se anuncia como validada. Esa revisión requiere
el dispositivo y una persona que lo pruebe; una captura por sí sola no la reemplaza.

### Publicación

Ejecutar las suites existentes y las nuevas apropiadas sobre la ROM final. Usar
pruebas con entradas de mando para los recorridos completos y comprobaciones de
datos para mapas/contraseñas. Los informes identifican commit, ROM y emulador.

Hasta que la aventura esté lista, `dist/`, `VERSION` y el enlace de descarga siguen
apuntando a la entrega estable. Las ROM de prototipo se generan en `build/`.
Al publicar, seguir [el proceso de entrega](DESARROLLO.md): conservar la entrega
anterior fuera del repositorio, empaquetar solo la ROM actual, instrucciones y SHA-256,
y verificar que el enlace directo devuelve exactamente ese binario.

La entrega completa requiere: seis fases terminables, tres personajes, tres tareas
narrativas con ayuda, final y epílogo, recuperación por contraseña, acceso a los
juegos originales, documentación actualizada y validación portátil registrada.
Un prototipo se identifica como tal y no reemplaza silenciosamente esa entrega.

## 13. Fuera de esta primera entrega

Diez mundos, diez motores diferentes, cooperativo simultáneo, combate con
profundidad tipo beat 'em up, inventario amplio, armas desbloqueables por jefe,
mundo abierto, decisiones que creen campañas completas distintas, doblaje, guardado
por batería y expansiones de audio. Tampoco se aumenta la duración repitiendo los
tres minijuegos entre todas las fases.

Tras completar y probar esta campaña se puede elegir una ampliación: estudio
embrujado, jungla de decorados, contrarreloj, tomas aleatorias o modo de pasar la
consola. Cada una debe contribuir a una nueva idea de sketch y reutilizar la base
estable en lugar de reiniciar el proyecto.

## 14. Próxima acción concreta

Implementar **P0 y P1**: una sala de prueba con Chucho que permita desplazarse,
saltar, atacar, recibir daño, reiniciar y pausar con cámara. Entregar su ROM interna
y un informe de memoria. Después construir **una sola toma completa** según P2.

El objetivo de esa primera toma es demostrar tres cosas juntas: que se siente bien
jugar, que el minijuego encaja en la producción del sketch y que el remate recompensa
haberlo completado. Solo entonces se escala al resto de la campaña.
