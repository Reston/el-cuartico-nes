$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot 'build') | Out-Null
python assets/generate.py
if ($LASTEXITCODE) { throw 'Asset generation failed' }
python tools/generate_music.py
if ($LASTEXITCODE) { throw 'Music generation failed' }
$bin = Join-Path $PSScriptRoot 'tools/cc65/bin'
& "$bin/cc65.exe" -t nes -Oirs --add-source -g src/game.c -o src/game.s
if ($LASTEXITCODE) { throw 'C compilation failed' }
& "$bin/ca65.exe" -t nes -g src/game.s -o src/game.o
if ($LASTEXITCODE) { throw 'Game assembly failed' }
& "$bin/ca65.exe" -t nes -g src/start.s -o src/start.o
if ($LASTEXITCODE) { throw 'Startup assembly failed' }
& "$bin/ld65.exe" -C src/nes.cfg src/start.o src/game.o tools/cc65/lib/nes.lib -o build/el-cuartico.nes -m build/el-cuartico.map -Ln build/el-cuartico.lbl --dbgfile build/el-cuartico.dbg
if ($LASTEXITCODE) { throw 'Link failed' }
Write-Output 'Built build/el-cuartico.nes'
