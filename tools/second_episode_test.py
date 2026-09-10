"""Play episode two using controller input; never write RAM or load a state."""
import hashlib,struct
import retro_harness as h
from play_helpers import read as r,task_keys,district_go
from episode2_helpers import select,launch,complete_episode,complete_current,game_keys,rhythm_keys,search_keys,linked_keys,KEYS,cursor_keys
report=[]
def check(ok,label):
    line=('PASS ' if ok else 'FAIL ')+label;print(line,flush=True);report.append(line)
    (h.root/'build/second-episode-tests.txt').write_text('\n'.join(report)+'\n');assert ok,label

def word(n):return r(n)+256*r(n,1)
def row(n):return bytes(r(n,i) for i in range(32)).decode('ascii').strip()
def peak():
    ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
    return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
def leave():h.press(3);h.press(0);assert r('mode')==0

def retry():
    h.press(3);h.press(8);assert r('mode')==9;h.press(8)

def go(x,y):
    for _ in range(400):
        px,py=r('px'),r('py');tx,ty=x,y
        if py<140 and ((px<128)!=(x<128)):tx,ty=(32 if px<128 else 208),144
        if abs(px-tx)>2:k=7 if px<tx else 6
        elif abs(py-ty)>2:k=5 if py<ty else 4
        else:return
        h.frames(1,[k])
    raise AssertionError('Could not reach station')

h.frames(90);complete_episode()
check(r('episode')==0 and r('remix_unlocked')==0,'First episode leads to a second episode before unlocking Remix')
prior=word('score');h.press(8)
check(r('mode')==0 and r('episode')==1 and r('completed')==0,'A continues into episode two with three fresh missions')
check(word('score')==prior and all(r('first_medals',i)==3 for i in range(3)),'Continuing retains score and first-episode medals')
h.screenshot('episode2-hub.png')
# Holding the menu launch cannot dismiss the mission brief.
for host in range(3):
    select(host);h.frames(90,[8]);check(r('mode')==9,'Held launch stays on untimed mission brief '+str(host))
    snapshot=(r('seconds'),r('completed'),word('score'));h.frames(3700)
    check(snapshot==(r('seconds'),r('completed'),word('score')),'Mission brief consumes no time or campaign progress '+str(host))
    h.screenshot('episode2-brief-'+str(host)+'.png');h.press(0)
    check(r('mode')==0 and r('host')==host,'B leaves the brief at the same selection '+str(host))
    h.press(4);check(r('mode')==8,'Episode-two help remains available '+str(host));h.press(0)

launch(0)
check(r('link_mask')==0 and r('alarm',0)>0 and not any(r('alarm',i) for i in (1,2,3)),'Only power is repairable when a broadcast begins')
go(208,64);h.press(8)
check(not r('task_active') and r('repairs')==0,'Camera cannot be repaired before power')
retry()
for _ in range(24*60):
    if r('health')<5:break
    h.frames(1)
check(r('health')==4 and r('alarm',0)>0 and r('link_mask')==0,'An expired power fault stays repairable without a dependency deadlock')
retry()
trace=[];frozen=False;maxsprites=0
for f in range(15000):
    if r('mode')!=1:break
    if not r('hud_on'):h.frames(1);continue
    if r('task_active') and not frozen:
        before=(r('seconds'),r('tick'),r('health'),r('link_mask'))+tuple(r('alarm',i) for i in range(4))
        h.frames(4800)
        check(before==(r('seconds'),r('tick'),r('health'),r('link_mask'))+tuple(r('alarm',i) for i in range(4)),'Linked repairs retain the unlimited puzzle timer')
        h.press(3);h.press(2);h.frames(120);h.press(0);h.press(3)
        check(r('task_active') and r('link_mask')==before[3],'Pause and panel help preserve the dependency chain');frozen=True
    old,station=r('repairs'),r('repair_task');h.frames(1,linked_keys(f))
    if r('repairs')!=old:
        trace.append(station)
        if station==0:check(r('link_mask')==1 and r('alarm',1)>0 and r('alarm',2)>0,'Power opens both camera and mixer in broadcast '+str(old//4+1))
        if r('link_mask')==7:check(r('alarm',3)>0,'Both middle repairs unlock the transmission')
    if r('mode')==1 and not r('task_active'):
        maxsprites=max(maxsprites,peak())
        if r('link_mask')==1 and r('feedback')==12:h.screenshot('episode2-chucho.png')
h.frames(25)
check(trace==[0,1,2,3,0,2,1,3,0,1,2,3],'Three complete broadcasts support both middle-station orders')
check(r('mode')==4 and r('completed')==1 and r('medals',0)==3,'Linked broadcast earns its stamp and clean medal')
check(maxsprites<=8,'Linked station markers respect the sprite scanline budget');h.press(8)

# Release a held note early, then retry the mission through the normal pause UI.
launch(1)
for f in range(3000):
    i=r('cue_head')
    if i<3 and r('note_hold',i) and r('note_age',i)==90:
        h.frames(1,[KEYS[r('note_key',i)]]);break
    h.frames(1,rhythm_keys())
check(r('hold_slot')<3 and r('hold_left')==30,'A long note starts a real hold instead of awarding an instant hit')
before=r('hits');h.frames(8,[KEYS[r('note_key',r('hold_slot'))]]);h.frames(1)
check(r('misses')==1 and r('hits')==before and r('hold_slot')==255,'Releasing a long note early produces one miss and no hit')
retry();acts=set();pcm_hashes=set();held=0;pause_done=False;maxsprites=0;badframes=0
for f in range(15000):
    if r('mode')!=2:break
    if not r('hud_on'):h.frames(1);continue
    act=r('music_act')
    if not r('cue_demo') and act not in acts:
        acts.add(act);check(r('music_track')==8+act,'The longer routine has its own composition in act '+str(act+1))
        h.audio_samples.clear();h.capture_audio=True;h.frames(70);h.capture_audio=False
        pcm=bytes(h.audio_samples);pcm_hashes.add(hashlib.sha256(pcm).hexdigest())
        values=struct.unpack('<'+'h'*(len(pcm)//2),pcm)
        check(len(pcm)>1000 and 100<max(abs(v) for v in values)<32767,'New composition produces audible unclipped audio '+str(act+1))
    if r('hold_slot')<3 and not pause_done:
        h.press(3);snapshot=tuple(r(n) for n in ('hold_left','hits','misses','song_step','song_tick','rhythm_phase'))
        check(r('paused')==1 and r('misses')==0,'A held note can be paused without registering a release miss')
        h.frames(60);h.press(2);h.frames(90);h.press(0);h.press(3)
        check(r('hold_resume')==1 and snapshot==tuple(r(n) for n in ('hold_left','hits','misses','song_step','song_tick','rhythm_phase')),'Resuming a paused hold waits for the matching button without losing timing')
        h.frames(180)
        check(r('misses')==0 and r('hold_left')==snapshot[0],'The player can re-grip the held button after consulting help')
        pause_done=True;h.screenshot('episode2-hold-resume.png')
    old=r('hold_slot');a=r('anim_tick');h.frames(1,rhythm_keys())
    if r('mode')==2 and r('hud_on'):
        maxsprites=max(maxsprites,peak())
        badframes+=((r('anim_tick')-a)%256!=1)
        if r('hold_slot')<3 and r('hold_left')==18:h.screenshot('episode2-estefania.png')
    if old<3 and r('hold_slot')==255:held+=1
h.frames(25)
check(r('hits')==49 and r('misses')==0 and r('medals',1)==3,'The full routine completes 49 clean hits and keeps its perfect medal')
check(acts=={0,1,2} and len(pcm_hashes)==3 and held>=9,'All three acts include held notes and distinct music')
check(maxsprites<=8 and badframes==0,'Sustained notes preserve one update per frame and the sprite budget')
h.screenshot('episode2-rhythm-result.png');h.press(8)

launch(2)
# Exercise the boundary where a prop's box and a top-row face can meet.
overlap=None
for attempt in range(12):
    for item in range(2):
        for person in range(r('crowd_count')):
            x=max(r('prop_x',item)-8,min(r('npc_x',person),r('prop_x',item)+8))
            if r('npc_y',person)==96 and abs(x-r('npc_x',person))<=10:
                overlap=(x,person);break
        if overlap:break
    if overlap:break
    retry();h.frames(25)
assert overlap, 'No overlapping face/prop boundary was generated'
x,person=overlap
for _ in range(1000):
    if (r('cursor_x'),r('cursor_y'))==(x,86):break
    h.frames(1,cursor_keys(x,86))
h.frames(6,[0]);shown=r('zoom_npc');before=(r('found'),r('misses'),r('collected_props'))
assert shown<24 and shown==r('hover_npc')
h.frames(5,[0,8]);h.frames(10)
check(r('collected_props')==before[2] and (r('found')==before[0]+1 or r('misses')==before[1]+1),'A confirms the magnified face even where an optional prop is nearby')
retry();h.frames(25)
# Collect a prop, revisit it and retry: no bonus farming or stale inventory.
for f in range(1000):
    if r('prop_mask'):break
    h.frames(1,search_keys(True))
check(r('prop_mask')==1 and r('collected_props')==1 and r('clue_timer')>0,'A hidden prop awards a clue and increments optional inventory')
check('PISTA:' in row('status_row'),'The found prop reveals a readable location clue')
before=word('attempt_score');h.frames(2);h.press(8)
check(r('collected_props')==1 and word('attempt_score')==before,'An already collected prop cannot award its bonus twice')
retry();check(r('collected_props')==0 and r('prop_mask')==0,'Retry clears only the current search inventory')
# Items must remain optional; complete once without picking any up.
complete_current(2,False)
check(r('collected_props')==0 and r('episode')==1 and r('mode')==5,'Daniel can complete the mission with no optional props')
check(r('remix_unlocked')==1 and r('completed')==7,'Finishing both episodes unlocks Remix')
h.screenshot('episode2-ending.png')
h.press(8)
check(r('episode')==0 and r('remix')==1 and r('completed')==0 and word('score')==0,'Remix restarts the whole two-episode campaign')
complete_episode();h.press(8)
check(r('episode')==1 and r('remix')==1,'Remix also advances into the second episode')
launch(2);worlds=set();maxsprites=0;checked_revisit=False
for f in range(12000):
    if r('mode')!=3:break
    if not r('hud_on'):h.frames(1);continue
    if r('round_no') not in worlds:
        worlds.add(r('round_no'));h.frames(3);h.screenshot('episode2-objects-'+str(r('round_no'))+'.png');check(r('crowd_count')<=24 and r('prop_mask')==0,'Each new world has a fresh optional prop pair')
    if r('round_no')==1 and r('prop_mask')==1 and not checked_revisit:
        at=r('district');mask=r('prop_mask');total=r('collected_props');district_go(at^1);district_go(at)
        check(r('prop_mask')==mask and r('collected_props')==total,'Collected props stay gone when returning to their district')
        check(row('status_row').endswith(str(r('target_district')+1)),'Prop clue names the correct numbered district')
        checked_revisit=True
    h.frames(1,search_keys(True))
    if r('mode')==3:
        maxsprites=max(maxsprites,peak())
        if r('clue_timer')==200:h.screenshot('episode2-daniel.png')
h.frames(25)
check(r('found')==3 and r('collected_props')==6 and r('medals',2)==3,'All six optional props can be collected with all three clean searches')
check(maxsprites<=8,'Props, cursor, birds and lens fit the sprite scanline budget')
h.screenshot('episode2-props-result.png');h.press(8)
for host in (1,0):
    launch(host);complete_current(host,True)
    check(r('medals',host)==3,'Episode-two mission remains solvable in Remix: '+str(host))
    if r('mode')==4:h.press(8)
check(r('mode')==5 and r('completed')==7 and r('episode')==1,'A full Remix campaign reaches the second finale')
h.press(3)
check(r('mode')==0 and r('episode')==0 and r('remix')==0 and word('score')==0,'Start at the finale begins a fresh normal campaign')
h.core.retro_reset();h.frames(90)
check(r('mode')==0 and r('episode')==0 and r('completed')==0 and r('remix_unlocked')==0,'Console reset discards session progress without saving')
h.close()
