"""Ejecuta las pruebas sobre la Ãºltima compilaciÃ³n, sin descargar herramientas."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
for script in ['menu_test.py', 'campaign_test.py', 'mmc5_test.py', 'polish_test.py', 'plaza_music_test.py', 'expansion_test.py', 'repair_panel_test.py', 'episode_test.py', 'intro_test.py', 'presentation_test.py', 'second_episode_test.py', 'usability_test.py', 'reference_music_test.py']:
    subprocess.run([sys.executable, str(root / 'tools' / script)], cwd=root, check=True)
for actor in range(3):
    subprocess.run([sys.executable, str(root/'tools/adventure_animation_test.py'), str(actor)], cwd=root, check=True)
    subprocess.run([sys.executable, str(root/'tools/adventure_test.py'), str(actor)], cwd=root, check=True)
subprocess.run([sys.executable, str(root/'tools/adventure_polish_test.py')], cwd=root, check=True)
if '--mesen' in sys.argv:
    for script in ['campaign_mesen.lua', 'presentation_mesen.lua', 'second_episode_mesen.lua', 'usability_mesen.lua', 'reference_music_mesen.lua', 'adventure_mesen.lua']:
        subprocess.run([sys.executable, str(root / 'tools/run_test.py'), str(root / 'tools' / script)], cwd=root, check=True)
