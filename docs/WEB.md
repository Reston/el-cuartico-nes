# Jugar en el navegador

Sitio público: **https://reston.github.io/el-cuartico-nes/**

GitHub Pages sirve una página estática y la ROM de **main** desde `gh-pages`, sin
servidor de juego, base de datos ni dominio de pago. El emulador corre en el
dispositivo del jugador. El alojamiento es gratuito para este repositorio público,
con los [límites de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## Controles

- Flechas: moverse o elegir personaje; arriba abre su ayuda desde el menú.
- X: A de NES, confirmar o actuar según el minijuego.
- Z: B de NES, correr con Chucho, lupa con Daniel o volver según el contexto.
- Enter: Start, empezar y pausar.
- Shift: Select, cambiar personaje o abrir los controles durante la pausa.

El emulador ofrece controles táctiles en móvil, mandos y pantalla completa.
El juego es **¡Estamos grabando!**, con seis misiones, dos episodios y Remix.
El progreso dura la sesión; no hay contraseña ni guardado por batería. Para
continuar otro día, usa Guardar Estado en el emulador y conserva el archivo;
Cargar Estado lo recupera usando la misma versión de la ROM. No se promete
sincronización entre dispositivos ni compatibilidad de estados entre versiones.

## Preparar y probar

Requiere Node.js; no hace falta instalar paquetes npm. Desde la raíz:

```powershell
node tools/prepare_web.mjs
python -m http.server 8765 --directory build/web --bind 127.0.0.1
```

Abre `http://127.0.0.1:8765/`. No abras `index.html` como un archivo local.
El preparador lee `VERSION`, la ROM y su checksum directamente del commit de
`origin/main` con Git, aunque la rama de trabajo sea otra. Comprueba cabecera MMC5,
tamaño y SHA-256. Para actualizar esa referencia antes de una prueba, usa
`git fetch origin main`.
Genera `build/web/` con los archivos de `web/`, la ROM, su checksum, una imagen
del menú y la licencia. Los enlaces de código y guía apuntan al commit de main
del que procede la ROM. La captura del menú es `menu-footer-v0.13.1.png` de main;
la versión del juego cargado se muestra sobre la pantalla. Los cambios
experimentales de otras ramas no se publican como el juego principal.

Se carga **EmulatorJS 4.2.3 / FCEUmm**, fijado a esa versión, desde su CDN oficial
solo al pulsar Jugar ahora. Por tanto, el primer inicio necesita conexión y acceso
a `cdn.emulatorjs.org`. La ROM y la página se alojan en GitHub Pages. Si falla el
emulador, la página ofrece reintentar o descargar la ROM. NES funciona sin BIOS;
se desactivan los hilos para no requerir cabeceras COOP/COEP que Pages no configura.

## Publicar una actualización

Primero publica la nueva versión estable, incluidos `VERSION` y `dist/`, en
**main**. Desde la rama que contiene las herramientas del sitio:

```powershell
./tools/publish_web.ps1
```

El publicador sube la rama actual con el código del sitio, actualiza `origin/main`
y empaqueta exclusivamente la ROM de main. Publica los archivos generados en
`gh-pages` mediante un commit normal, sin forzar el historial. Usa un checkout
aislado dentro de `build/`; no cambia la rama de trabajo ni fusiona cambios en
`main`. Un push concurrente causa un fallo seguro; vuelve a ejecutar el comando.
No publica un árbol de fuente con cambios pendientes. No usa la ROM de la rama
actual, ni una compilación experimental de `build/`.

Configuración inicial de GitHub: **Settings → Pages → Deploy from a branch →
gh-pages → /(root)**. Una vez habilitado, cada publicación en esa rama actualiza
el sitio automáticamente. El enlace público puede tardar unos minutos en reflejar
el nuevo commit. `gh-pages` contiene solamente el sitio generado; sus cambios no
deben editarse a mano.

Emulador y documentación: [EmulatorJS](https://emulatorjs.org/),
[FCEUmm](https://github.com/libretro/libretro-fceumm). El código correspondiente
a la ROM está enlazado desde el pie de la página; el proyecto usa GNU GPL v3.
