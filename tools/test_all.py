"""Ejecuta las pruebas sobre la última compilación, sin descargar herramientas."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
for script in ['menu_test.py', 'campaign_test.py', 'mmc5_test.py', 'polish_test.py', 'plaza_music_test.py', 'expansion_test.py', 'repair_panel_test.py', 'episode_test.py', 'intro_test.py', 'presentation_test.py', 'second_episode_test.py']:
    subprocess.run([sys.executable, str(root / 'tools' / script)], cwd=root, check=True)
if '--mesen' in sys.argv:
    for script in ['campaign_mesen.lua', 'presentation_mesen.lua', 'second_episode_mesen.lua']:
        subprocess.run([sys.executable, str(root / 'tools/run_test.py'), str(root / 'tools' / script)], cwd=root, check=True)
