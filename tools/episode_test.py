"""Controller-driven trial episode: hub, events, acts, medals and remix."""
import hashlib
import struct
import retro_harness as h
from play_helpers import read as r, repair_keys, district_go, start_search_from_intro
from episode2_helpers import complete_episode
report=[]
def check(ok,label):
 line=('PASS ' if ok else 'FAIL ')+label;print(line,flush=True);report.append(line)
 (h.root/'build/episode-tests.txt').write_text('\n'.join(report)+'\n');assert ok,label

def word(n):return r(n)+256*r(n,1)
def peak():
 ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
 return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
def go(x,y):
 for _ in range(300):
  a,b=r('px'),r('py')
  if a==x and b==y:return
  h.frames(1,[7 if a<x else 6] if a!=x else [5 if b<y else 4])
 raise AssertionError('Studio approach is blocked')
def rhythm_keys():
 if r('cue_demo'):return [8]
 i=r('cue_head')
 return [[8,0,6,7,4,5][r('cue_key')]] if i<3 and r('note_age',i)==90 else []
def search_keys():
 if r('search_wait') or r('feedback'):return []
 d,t=r('district'),r('target_district')
 if d!=t:return [7 if d%2<t%2 else 6] if d%2!=t%2 else [5 if d<t else 4]
 n=r('target');x,y=r('npc_x',n),r('npc_y',n)+4
 if r('cursor_x')!=x:return [7 if r('cursor_x')<x else 6]
 if r('cursor_y')!=y:return [5 if r('cursor_y')<y else 4]
 return [8]

h.frames(90)
for host in range(3):
 h.press(0);check(r('mode')==6,'B opens the walkable studio')
 go(32+host*88,104);h.frames(3)
 check(r('lounge_near')==host,'Walking reaches host '+str(host))
 check(peak()<=8,'Studio gathering respects sprite scanline budget')
 h.screenshot('episode-studio.png')
 h.press(8)
 if host==2:start_search_from_intro()
 check(r('mode')==host+1,'Studio interaction launches host '+str(host))
 h.press(3);h.press(0)

for remixed in (False,True):
 check(bool(r('remix'))==remixed,'Campaign uses the requested standard/remix rules')
 for host in range(3):
  while r('host')!=host:h.press(7)
  h.press(8)
  if host==2:start_search_from_intro()
  events=set();acts=set();music={};pcm_hashes=set();targets=set();maxsprites=0;bonus=0;held=False
  seen_progress=set();seen_worlds=set()
  for f in range(10000):
   if r('mode') not in (1,2,3):break
   if not r('hud_on'):h.frames(1);continue
   if host==0:
    event=r('studio_event')
    if event and event not in events:
     events.add(event);h.frames(6);h.screenshot('episode-event-'+str(event)+'.png')
    if remixed and r('task_active') and not held:
     snapshot=(r('seconds'),r('health'),r('tick'))+tuple(r('alarm',i) for i in range(4))
     h.frames(4800)
     check(snapshot==(r('seconds'),r('health'),r('tick'))+tuple(r('alarm',i) for i in range(4)),'Remix repairs also freeze clocks and fault deadlines for 80 seconds')
     held=True
    if r('task_active') and r('repair_task')==0:targets.add(tuple(r('task_order',i) for i in range(3)))
    if r('task_active'):seen_progress.add((r('repair_task'),r('task_progress')))
    keys=repair_keys(f)
    before=word('attempt_score');old_combo=r('combo');old_repairs=r('repairs');station=r('repair_task');special=r('event_station')
   elif host==1:
    act=r('music_act')
    if act not in acts:
     acts.add(act);h.frames(3);h.screenshot('episode-act-'+str(act+1)+'.png')
     music[act]=r('music_track')
     if act:
      check(r('count_in')>100 and not any(r('note_live',i) for i in range(3)),'Act '+str(act+1)+' starts with clear notes and a fresh count-in')
      h.press(3);state=(r('count_in'),r('song_tick'),r('song_step'));h.frames(60)
      check(state==(r('count_in'),r('song_tick'),r('song_step')),'Act '+str(act+1)+' count-in pauses with music');h.press(3)
     h.audio_samples.clear();h.capture_audio=True;h.frames(80);h.capture_audio=False
     pcm=bytes(h.audio_samples);pcm_hashes.add(hashlib.sha256(pcm).hexdigest())
     samples=struct.unpack('<'+'h'*(len(pcm)//2),pcm)
     check(len(pcm)>1000 and 100<max(abs(v) for v in samples)<32767,'Musical act produces audible unclipped audio')
    keys=rhythm_keys()
   else:
    world=r('round_no')
    if world not in seen_worlds:
     seen_worlds.add(world)
     check(r('crowd_count')==(16 if remixed else 12)+world*4,'Crowd size matches campaign rules in world '+str(world+1))
    keys=search_keys()
   h.frames(1,keys)
   if host==0 and event and station==special and r('repairs')>old_repairs:
    check(word('attempt_score')>=before+old_combo*100+200,'Resolving the studio event awards its bonus');bonus+=1
   if r('mode') in (1,2,3) and r('hud_on'):maxsprites=max(maxsprites,peak())
  h.frames(30)
  check(bool(r('completed')&(1<<host)),'Host '+str(host)+' completes '+('remix' if remixed else 'standard')+' campaign')
  check(maxsprites<=8,'New effects stay inside eight sprites per scanline')
  check(r('medals',host)==3,'A clean run retains a perfect medal for host '+str(host))
  if host==0:
   check(events=={1,2,3} and bonus==3,'All three studio events occur and can be resolved')
   check(len(targets)>=2,'Cable arrangements vary across repairs')
   if remixed:check((1,2) in seen_progress and (2,3) in seen_progress,'Remix extends camera and mixer puzzles without adding a timer')
  if host==1:
   check(acts=={0,1,2} and music=={0:2,1:6,2:7},'Three musical acts use three separate compositions')
   check(len(pcm_hashes)==3,'The three act recordings have distinct audio output')
  if host<2:h.press(3)
 check(r('mode')==5 and r('episode')==0,'Three victories reach the first episode closure')
 h.frames(140);h.press(0);check(r('finale_cheer')>90 and r('mode')==5,'B starts applause without leaving the finale')
 h.screenshot('episode-finale.png');h.frames(45)
 check(peak()<=8,'Finale celebration respects the scanline limit')
 if not remixed:
  h.press(8);check(r('episode')==1,'A continues from the first episode into the live broadcast')
  complete_episode(props=True);check(r('remix_unlocked')==1,'Finishing both episodes unlocks Remix');h.press(8)
 else:h.press(3)
 check(r('mode')==0 and r('completed')==0 and all(r('medals',i)==0 for i in range(3)),'A new episode resets stamps and medals')
check(r('remix')==0,'Start at the finale returns to the standard campaign')
h.press(8)
for f in range(5000):
 if r('repairs')==3 and r('hud_on') and not r('task_active'):break
 h.frames(1,repair_keys(f) if r('hud_on') else [])
check(r('studio_event')!=0,'A fresh studio event can be left unresolved')
h.frames(1150)
check(r('studio_event')==0,'An expired event clears its prompt and lighting state')
h.close()
