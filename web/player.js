/* EmulatorJS 4.2.3 uses FCEUmm, the same core used to validate this MMC5 ROM. */
(() => {
  'use strict';
  const game = window.CUARTICO_GAME;
  const status = document.querySelector('#status');
  const error = document.querySelector('#load-error');
  let loading = false;
  let timer;

  document.querySelector('#version').textContent = `v${game.version} · NES`;
  document.querySelector('#download').href = game.rom;
  document.querySelector('#source').href = game.source;
  document.querySelector('#guide').href = game.guide;

  function failed() {
    clearTimeout(timer);
    status.textContent = 'NO SE PUDO CARGAR';
    error.hidden = false;
  }

  function start() {
    if (loading) return;
    loading = true;
    document.querySelector('#launch').hidden = true;
    status.textContent = 'CARGANDO EL JUEGO…';
    window.EJS_player = '#game';
    window.EJS_core = 'fceumm';
    window.EJS_gameUrl = new URL(game.rom, document.baseURI).href;
    window.EJS_gameName = `El Cuartico v${game.version}`;
    window.EJS_pathtodata = 'https://cdn.emulatorjs.org/4.2.3/data/';
    window.EJS_language = 'es-ES';
    window.EJS_color = '#f4c928';
    window.EJS_backgroundColor = '#101010';
    window.EJS_startOnLoaded = true;
    window.EJS_threads = false;
    window.EJS_volume = 0.5;
    // RetroPad B maps to NES B; RetroPad A maps to NES A.
    window.EJS_defaultControls = {
      0: {
        0: { value: 'z', value2: 'BUTTON_2' },
        2: { value: 'shift', value2: 'SELECT' },
        3: { value: 'enter', value2: 'START' },
        4: { value: 'up arrow', value2: 'DPAD_UP' },
        5: { value: 'down arrow', value2: 'DPAD_DOWN' },
        6: { value: 'left arrow', value2: 'DPAD_LEFT' },
        7: { value: 'right arrow', value2: 'DPAD_RIGHT' },
        8: { value: 'x', value2: 'BUTTON_1' }
      },
      1: {},
      2: {},
      3: {}
    };
    window.EJS_onGameStart = () => {
      clearTimeout(timer);
      error.hidden = true;
      status.textContent = 'EN JUEGO';
    };
    const loader = document.createElement('script');
    loader.src = `${window.EJS_pathtodata}loader.js`;
    loader.onerror = failed;
    timer = setTimeout(failed, 60000);
    document.body.appendChild(loader);
  }

  document.querySelector('#play').addEventListener('click', start);
  document.querySelector('#retry').addEventListener('click', () => location.reload());
})();
