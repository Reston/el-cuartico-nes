"""Download portable development tools into this project only."""
import sys,urllib.request,zipfile,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
tools=root/'tools'
def install(url,name):
    print('Downloading',name)
    archive=tools/(name+'.zip')
    urllib.request.urlretrieve(url,archive)
    with zipfile.ZipFile(archive) as z:z.extractall(tools/name)
install('https://downloads.sourceforge.net/project/cc65/cc65-snapshot-win64.zip','cc65')
if '--test-tools' in sys.argv:
    install('https://github.com/nesdev-org/MesenCE/releases/download/2.2.1/Mesen_2.2.1_Windows.zip','mesen')
    install('https://buildbot.libretro.com/nightly/windows/x86_64/latest/fceumm_libretro.dll.zip','fceumm')
    (tools/'mesen/settings.json').write_text(json.dumps({'Nes':{'Port1':{'Type':'NesController'}},'Debug':{'ScriptWindow':{'AllowIoOsAccess':True}}}))
print('Tools ready. Run build.ps1.')
