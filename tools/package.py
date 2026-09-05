"""Publica únicamente la ROM actual y su checksum en dist/."""
from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parents[1]
version = (root / 'VERSION').read_text().strip()
if not re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,2}', version):
    raise ValueError('VERSION debe contener una versión numérica')
data = (root / 'build/el-cuartico.nes').read_bytes()
if data[:4] != b'NES\x1a' or ((data[6] >> 4) | (data[7] & 240)) != 5:
    raise ValueError('Se esperaba una ROM iNES con mapper MMC5')
if len(data) != 16 + data[4] * 16384 + data[5] * 8192:
    raise ValueError('Tamaño de ROM incorrecto')
dist = root / 'dist'
dist.mkdir(exist_ok=True)
name = f'el-cuartico-v{version}-mmc5.nes'
older = [p for p in dist.glob('*.nes') if p.name != name]
if older:
    raise SystemExit('Mueve las ROM anteriores fuera del repositorio antes de publicar: ' + ', '.join(p.name for p in older))
(dist / name).write_bytes(data)
(dist / 'SHA256.txt').write_text(hashlib.sha256(data).hexdigest() + '  ' + name + '\n')
print(f'ROM publicada: dist/{name} ({len(data)} bytes)')
