"""Frame-level regression for character selection, including wrap and rapid taps."""
import retro_harness as h
from play_helpers import start_from_intro
report=[]
def check(ok,msg):
 line=('PASS ' if ok else 'FAIL ')+msg
 print(line,flush=True);report.append(line)
 (h.root/'build/menu-tests.txt').write_text('\n'.join(report)+'\n')
 assert ok,msg
def rowbytes():
 return bytes(h.C.c_uint8.from_address(h.ram+h.labels['_menu_rows']+i).value for i in range(96))
def header():
 raw,w,ht,pitch,fmt=h.screen
 return raw[56*pitch:80*pitch]
def footer_matches():
 raw,w,ht,pitch,fmt=h.screen
 size=4 if fmt==1 else 2
 background=raw[224*pitch:224*pitch+size]
 text="< > ELIGE A:JUEGA B:ESTUDIO"
 row=(' '*((32-len(text))//2)+text).ljust(32)
 graphics=(h.root/'assets/mmc5.chr').read_bytes()
 for x,ch in enumerate(row):
  tile=graphics[ord(ch)*16:(ord(ch)+1)*16]
  for y in range(8):
   for bit in range(8):
    ink=((tile[y]|tile[y+8])>>(7-bit))&1
    offset=(224+y)*pitch+(x*8+bit)*size
    if (raw[offset:offset+size]!=background)!=bool(ink):return False
 return True

h.frames(90);base=header();expected=0;bad=[];stalls=[]
check(footer_matches(),'Footer pixels match the font bank at startup')
names=['CHUCHO','ESTEFANIA','DANIEL']
titles=['LA GRABACION','EL SKETCH','DONDE ESTA DANIEL?']
goals=['12 TOMAS EN VIVO','20 ACIERTOS','3 ENCUENTROS']
for step,key in enumerate([7,7,7,6,6,6,2,2,2]*4):
 expected=(expected+(-1 if key==6 else 1))%3
 for f in range(4):
  before=h.read('anim_tick');h.frames(1,[key] if f==0 else [])
  if header()!=base:bad.append((step,f))
  if (h.read('anim_tick')-before)%256!=1:stalls.append((step,f))
 # C centers with floor left padding (str.center differs for some odd lengths).
 wanted=b''.join(((' '*((32-len(s))//2)+s).ljust(32)).encode() for s in [titles[expected],names[expected],goals[expected]])
 assert h.read('host')==expected and rowbytes()==wanted,(step,expected,rowbytes())
 assert h.read('menu_dirty')==0
check(footer_matches(),'Footer remains readable after rapid character selection')
check(not bad,'Static menu art stays intact on all 144 frames of rapid selection')
check(not stalls,'Selection preserves continuous 60 Hz animation without resets or stalls')
check(True,'Left, Right and Select wrap correctly with complete centered labels and no stale text')
h.screenshot('menu-fixed.png')
h.press(8);start_from_intro();check(h.read('mode')==1,'A launches the selected Chucho game after repeated switching')
h.press(3);h.press(0);check(h.read('mode')==0,'Pause exit restores the complete menu')
check(footer_matches(),'Returning from gameplay restores the correct footer glyphs')
h.press(7);h.press(3);start_from_intro();check(h.read('mode')==2,'Start confirms Estefania after her title card')
h.press(3);h.press(0);h.press(7);h.press(8)
check(h.read('mode')==7,'Daniel opens his title card after returning and changing selection')
start_from_intro();check(h.read('mode')==3,'A starts searching from the title card')
h.close()
