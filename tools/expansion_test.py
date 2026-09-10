"""Controller-driven v0.8 world persistence, distractions and studio mechanics."""
import retro_harness as h
from play_helpers import read as r,district_go,target_area,start_from_intro
report=[]
def check(ok,msg):
 line=('PASS ' if ok else 'FAIL ')+msg;print(line,flush=True);report.append(line)
 (h.root/'build/expansion-tests.txt').write_text('\n'.join(report)+'\n');assert ok,msg
def boot(host):
 h.core.retro_reset();h.frames(90)
 for _ in range(host):h.press(7)
 h.press(8);h.frames(20)
 start_from_intro()
def pulse(key):h.frames(1,[key]);h.frames(1)
def go(x,y,studio=False):
 xn,yn=('px','py') if studio else ('cursor_x','cursor_y')
 for _ in range(500):
  a,b=r(xn),r(yn)
  if abs(a-x)<2 and abs(b-y)<2:return
  h.frames(1,[7 if a<x else 6] if abs(a-x)>=2 else [5 if b<y else 4])
 raise AssertionError('navigation timeout')
def peak():
 ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
 return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
def snap():return tuple(r(n,i) for n in ['crowd','npc_x','npc_y'] for i in range(r('crowd_count')))+(r('target'),)
boot(2)
for round_no in range(3):
 check(r('district_count')==1<<round_no,'Search '+str(round_no+1)+' has '+str(1<<round_no)+' connected screens')
 snapshots={};unique=0;banks=set()
 for district in range(1<<round_no):
  district_go(district);snapshots[district]=snap();banks.add(r('scene_bank'))
  unique+=sum(r('crowd',i)==0 for i in range(r('crowd_count')))
  h.screenshot('world-'+str(round_no+1)+'-'+str(district+1)+'.png')
  a=r('anim_tick');motion=set();max_sprites=0
  for _ in range(40):
   h.frames(1);max_sprites=max(max_sprites,peak())
   motion.add(tuple(h.C.c_uint8.from_address(h.ram+0x200+i).value for i in range(256)))
  assert (r('anim_tick')-a)%256==40 and max_sprites<=8
  if round_no:assert len(motion)>10
  tiles=[h.C.c_uint8.from_address(h.ram+0x201+i*4).value for i in range(64) if h.C.c_uint8.from_address(h.ram+0x200+i*4).value<240]
  assert 62 not in tiles and 63 not in tiles
  raw,w,ht,pitch,fmt=h.screen;footer=raw[224*pitch:232*pitch]
  for _ in range(40):
   h.frames(1,[0,7,5])
   assert h.screen[0][224*pitch:232*pitch]==footer
   visible=[h.C.c_uint8.from_address(h.ram+0x201+k*4).value for k in range(64) if h.C.c_uint8.from_address(h.ram+0x200+k*4).value<240]
   assert not any(t in visible for t in [44,45,46,47,60,61,62,63])
 check(unique==1,'Exactly one Daniel exists across the entire search world')
 check(len(banks)==1<<round_no,'Every district has its own landmark graphics')
 check(True,'Moving distractions and lens retain 60 Hz and eight-sprite scanline limit')
 for district in reversed(range(1<<round_no)):
  district_go(district);assert snap()==snapshots[district]
 check(True,'Revisiting every district preserves people and hiding position')
 check(True,'Exit strip stays unobstructed by cursor, arrows or birds during magnification')
 if round_no:
  district_go(0 if r('target_district') else 1);go(8,74);before=r('found');pulse(8)
  check(r('found')==before and r('misses')>0,'Empty selection in a district without Daniel cannot count as a find')
  h.frames(35)
 target_area();go(r('npc_x',r('target')),r('npc_y',r('target'))+4);h.frames(3,[0]);pulse(8)
 for _ in range(120):
  h.frames(1)
  if r('mode')!=3 or r('round_no')!=round_no and r('hud_on'):break
check(r('completed')==4 and r('found')==3,'Full exploration still earns Daniel stamp only after all three worlds')
h.close()
