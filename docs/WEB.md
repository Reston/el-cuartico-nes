# Jugar en el navegador

Sitio público: **https://reston.github.io/el-cuartico-nes/**

GitHub Pages sirve una página estática y la ROM actual desde `gh-pages`, sin
servidor de juego, base de datos ni dominio de pago. El emulador corre en el
dispositivo del jugador. El alojamiento es gratuito para este repositorio público,
con los [límites de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## Controles

- Flechas: moverse; arriba interactúa.
- X: A de NES, saltar y elegir.
- Z: B de NES, acción.
- Enter: Start, empezar y pausar.
- Shift: Select, cambiar actor o abrir el mapa según el contexto.

El emulador ofrece controles táctiles en móvil, mandos y pantalla completa.
La aventura conserva progreso con la contraseña que aparece al pulsar Start
en la mesa de ideas. Anótala antes de cerrar. No se promete guardado automático
de toda la aventura al cerrar una pestaña ni sincronización entre dispositivos.

## Preparar y probar

Requiere Node.js; no hace falta instalar paquetes npm. Desde la raíz:

```powershell
node tools/prepare_web.mjs
python -m http.server 8765 --directory build/web --bind 127.0.0.1
```

Abre `http://127.0.0.1:8765/`. No abras `index.html` como un archivo local.
El preparador comprueba cabecera MMC5, tamaño y SHA-256 de la ROM de `dist/`.
Genera `build/web/` con los archivos de `web/`, la ROM, su checksum, una imagen
del menú y la licencia. Los enlaces de código y guía apuntan al commit publicado.
La imagen del menú es una captura de v0.14.0; el juego cargado es la versión de
`VERSION`, mostrada sobre la pantalla. El menú conserva ese diseño.

Se carga **EmulatorJS 4.2.3 / FCEUmm**, fijado a esa versión, desde su CDN oficial
solo al pulsar Jugar ahora. Por tanto, el primer inicio necesita conexión y acceso
a `cdn.emulatorjs.org`. La ROM y la página se alojan en GitHub Pages. Si falla el
emulador, la página ofrece reintentar o descargar la ROM. NES funciona sin BIOS;
se desactivan los hilos para no requerir cabeceras COOP/COEP que Pages no configura.

## Publicar una actualización

Primero genera la ROM y confirma los cambios de fuente y `dist/` en Git:

```powershell
./build.ps1
git add <archivos-de-la-version>
git commit -m "Publicar nueva versión"
./tools/publish_web.ps1
```

El publicador sube la rama de fuente actual y publica los archivos generados en
`gh-pages` mediante un commit normal, sin forzar el historial. Usa un checkout
aislado dentro de `build/`; no cambia la rama de trabajo ni fusiona cambios en
`main`. Un push concurrente causa un fallo seguro; vuelve a ejecutar el comando.
No publica un árbol de fuente con cambios pendientes.

Configuración inicial de GitHub: **Settings → Pages → Deploy from a branch →
gh-pages → /(root)**. Una vez habilitado, cada publicación en esa rama actualiza
el sitio automáticamente. El enlace público puede tardar unos minutos en reflejar
el nuevo commit. `gh-pages` contiene solamente el sitio generado; sus cambios no
deben editarse a mano.

Emulador y documentación: [EmulatorJS](https://emulatorjs.org/),
[FCEUmm](https://github.com/libretro/libretro-fceumm). El código correspondiente
a la ROM está enlazado desde el pie de la página; el proyecto usa GNU GPL v3.
