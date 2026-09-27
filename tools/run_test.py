from pathlib import Path
import subprocess,re,sys,tempfile,json
root=Path(__file__).resolve().parents[1]
script=Path(sys.argv[1]) if len(sys.argv)>1 else root/'tools/smoke.lua'
# Wall-clock allowance is separate from each Lua replay's frame/progress checks.
seconds=120 if script.name=='adventure_mesen.lua' else (60 if script.name=='second_episode_mesen.lua' else 35)
with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.lua',dir=root/'tools',delete=False) as temp:
    temp.write('PROJECT_ROOT = '+json.dumps(root.as_posix()+'/',ensure_ascii=False)+'\n'+script.read_text(encoding='utf-8'))
    temp_path=Path(temp.name)
try:
    result=subprocess.run([str(root/'tools/mesen/Mesen.exe'),'--testRunner',str(root/'build/el-cuartico.nes'),str(temp_path),f'--timeout={seconds}','--enableStdout'],capture_output=True,text=True,timeout=seconds+10)
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
