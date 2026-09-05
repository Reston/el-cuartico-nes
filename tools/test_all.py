"""Ejecuta las pruebas sobre la última compilación, sin descargar herramientas."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
for script in ['menu_test.py', 'campaign_test.py', 'mmc5_test.py', 'polish_test.py', 'plaza_music_test.py', 'expansion_test.py', 'repair_panel_test.py']:
    subprocess.run([sys.executable, str(root / 'tools' / script)], cwd=root, check=True)
if '--mesen' in sys.argv:
    subprocess.run([sys.executable, str(root / 'tools/run_test.py'), str(root / 'tools/campaign_mesen.lua')], cwd=root, check=True)
