$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot 'build') | Out-Null
python assets/generate.py
if ($LASTEXITCODE) { throw 'Asset generation failed' }
python tools/generate_music.py
if ($LASTEXITCODE) { throw 'Music generation failed' }
$bin = Join-Path $PSScriptRoot 'tools/cc65/bin'
& "$bin/cc65.exe" -t nes -Oirs --add-source -g --code-name CLASSICCODE src/game.c -o src/game.s
if ($LASTEXITCODE) { throw 'C compilation failed' }
& "$bin/ca65.exe" -t nes -g src/game.s -o src/game.o
if ($LASTEXITCODE) { throw 'Game assembly failed' }
& "$bin/ca65.exe" -t nes -g src/start.s -o src/start.o
if ($LASTEXITCODE) { throw 'Startup assembly failed' }
foreach ($unit in @(@('adventure', 'ADVCODE', 'ADVRODATA'), @('adventure_ui', 'ADVUICODE', 'ADVUIRODATA'))) {
    $localArgs = @(); if ($unit[0] -eq "adventure") { $localArgs = @("-Cl") }
    & "$bin/cc65.exe" -t nes -Oirs -g @localArgs --code-name $unit[1] --rodata-name $unit[2] "src/$($unit[0]).c" -o "src/$($unit[0]).s"
    if ($LASTEXITCODE) { throw "Adventure compilation failed: $($unit[0])" }
    & "$bin/ca65.exe" -t nes -g "src/$($unit[0]).s" -o "src/$($unit[0]).o"
    if ($LASTEXITCODE) { throw 'Adventure assembly failed' }
}
& "$bin/ld65.exe" -C src/nes.cfg src/start.o src/game.o src/adventure.o src/adventure_ui.o tools/cc65/lib/nes.lib -o build/el-cuartico.nes -m build/el-cuartico.map -Ln build/el-cuartico.lbl --dbgfile build/el-cuartico.dbg
if ($LASTEXITCODE) { throw 'Link failed' }
Write-Output 'Built build/el-cuartico.nes'
