"""Controller-only repair-panel errors, cancellation, pause and completion."""
import retro_harness as h
from play_helpers import read as r,repair_keys,task_keys
report=[]
def check(ok,msg):
 line=('PASS ' if ok else 'FAIL ')+msg;print(line,flush=True);report.append(line)
 (h.root/'build/repair-panel-tests.txt').write_text('\n'.join(report)+'\n');assert ok,msg
def pulse(k):h.frames(1,[k]);h.frames(1)
def settle():
 for _ in range(30):
  h.frames(1)
  if r('hud_on'):return
 raise AssertionError('screen did not settle')
def peak():
 ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
 return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
h.frames(90);h.press(8);seen=set();cancelled=False;paused=False;maxsprites=0;stalls=0;target_changes=0
for f in range(7000):
 if r('mode')!=1:break
 if not r('hud_on'):h.frames(1);continue
 if r('task_active') and r('repair_task') not in seen:
  t=r('repair_task');seen.add(t);settle()
  clock=tuple(r(n) for n in ['seconds','tick'])
  h.frames(75)
  check(clock==tuple(r(n) for n in ['seconds','tick']),'Task '+str(t+1)+' freezes both seconds and fractional time')
  h.screenshot('repair-panel-'+str(t)+'.png')
  check(r('repairs')<12,'Station '+str(t+1)+' opens its own repair panel')
  if t==0:
   if r('task_order',r('task_cursor'))==0:pulse(5)
   pulse(8)
  elif t==1:pulse(8)
  elif t==2:
   while abs(r('task_value')-r('task_target'))<9:h.frames(1)
   pulse(8)
  else:
   start_frame=r('task_frame')+256*r('task_frame',1);waited=0;crossed_byte=False
   while not r('task_phase'):
    crossed_byte|=(r('task_frame')+256*r('task_frame',1))>=256
    h.frames(1);waited+=1
   check(start_frame+waited>=319 and crossed_byte,'Memory playback lasts over five seconds without an 8-bit timer overflow')
   pulse([6,7,4,5][(r('task_code',0)+1)%4])
  check(r('task_error')>0 and r('task_progress')==0,'Wrong input in task '+str(t+1)+' gives feedback without credit')
  if not cancelled:
   before=r('repairs');pulse(0);settle()
   check(not r('task_active') and r('repairs')==before,'B cancels a repair without awarding a take')
   pulse(8);settle();check(r('task_active') and not r('task_progress'),'Reopening starts a fresh repair puzzle')
   cancelled=True
  if not paused:
   alarms=tuple(r('alarm',i) for i in range(4));sec=r('seconds');h.frames(60)
   check(tuple(r('alarm',i) for i in range(4))==alarms and r('seconds')==sec,'Episode time and fault deadlines both freeze in the panel')
   pulse(3);saved=tuple(r(n) for n in ['task_value','task_progress','task_frame','task_phase','seconds'])
   h.frames(90,[7]);check(saved==tuple(r(n) for n in ['task_value','task_progress','task_frame','task_phase','seconds']),'Start pauses the repair panel and timer')
   pulse(3);paused=True
 before=r('anim_tick');old_task=r('repair_task');old_progress=r('task_progress');old_target=r('task_target')
 h.frames(1,repair_keys(f))
 if r('task_active') and old_task==2 and r('task_progress')>old_progress:
  assert 12<=r('task_target')<=51 and abs(r('task_target')-old_target)>=8
  target_changes+=1
 if r('mode')==1 and r('hud_on'):
  maxsprites=max(maxsprites,peak())
  visible=[h.C.c_uint8.from_address(h.ram+0x201+i*4).value for i in range(64) if h.C.c_uint8.from_address(h.ram+0x200+i*4).value<240]
  assert 62 not in visible and 63 not in visible
  # Loading a repair screen intentionally spans several frames; measure stable play separately.
  if r('task_active') and r('task_progress')>0:stalls+=(r('anim_tick')-before)%256!=1
check(target_changes>=2,'Mixer goal changes to a distinct reachable position after successful catches')
check(seen=={0,1,2,3},'All four repair minigames are exercised in one studio run')
check(maxsprites<=8,'Studio and repair panels respect eight sprites per scanline')
check(stalls==0,'Interactive repair panels update once per NTSC frame')
check(r('completed')==1 and r('repairs')==12,'Completing twelve puzzles earns Chucho stamp')
check(True,'No cart sprites appear during studio play or repair tasks')
h.core.retro_reset();h.frames(90);h.press(8)
for f in range(400):
 if r('task_active') and r('hud_on'):break
 h.frames(1,repair_keys(f) if r('hud_on') else [])
assert r('task_active')
saved=tuple(r(n) for n in ['seconds','tick','health','repairs'])+tuple(r('alarm',i) for i in range(4))
h.frames(5000)
check(r('mode')==1 and r('task_active') and saved==tuple(r(n) for n in ['seconds','tick','health','repairs'])+tuple(r('alarm',i) for i in range(4)),'Spending over 80 seconds in a repair does not consume time, hearts or fault deadlines')
hud=bytes(r('hud',i) for i in range(32))
check(b'SIN LIMITE' in hud,'Repair HUD clearly indicates there is no time limit')
pulse(0);settle();sec=r('seconds');h.frames(120)
check(not r('task_active') and r('seconds')==sec-2,'Leaving the panel resumes the studio clock at its previous value')
pulse(3);h.press(8);settle()
check(r('mode')==1 and not r('task_active') and r('repairs')==0,'Retry still returns to a fresh studio')
h.close()
