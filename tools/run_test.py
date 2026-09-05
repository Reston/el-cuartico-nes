from pathlib import Path
import subprocess,re,sys,tempfile,json
root=Path(__file__).resolve().parents[1]
script=Path(sys.argv[1]) if len(sys.argv)>1 else root/'tools/smoke.lua'
with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.lua',dir=root/'tools',delete=False) as temp:
    temp.write('PROJECT_ROOT = '+json.dumps(root.as_posix()+'/',ensure_ascii=False)+'\n'+script.read_text(encoding='utf-8'))
    temp_path=Path(temp.name)
try:
    result=subprocess.run([str(root/'tools/mesen/Mesen.exe'),'--testRunner',str(root/'build/el-cuartico.nes'),str(temp_path),'--timeout=35','--enableStdout'],capture_output=True,text=True,timeout=45)
finally:
    temp_path.unlink()
out=result.stdout+result.stderr
for i,match in enumerate(re.finditer(r'PNG(?::([a-z_]+))?:([0-9a-f]+)',out)):
    name=match[1] or 'title'
    (root/'build'/f'{name}.png').write_bytes(bytes.fromhex(match[2]))
out=re.sub(r'PNG(?::[a-z_]+)?:[0-9a-f]+','[screenshot saved]',out)
print(out)
print('Exit:',result.returncode)
(root/'build/test-results.txt').write_text(out+'\nExit: '+str(result.returncode))
sys.exit(result.returncode)
