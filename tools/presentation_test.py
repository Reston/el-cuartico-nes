"""Controller regressions for contextual help, pause and broadcast result cards."""
import hashlib
import json
import struct
import retro_harness as h
from play_helpers import read as r, task_keys, start_search_from_intro
report=[]

def check(ok,label):
    line=('PASS ' if ok else 'FAIL ')+label
    print(line,flush=True);report.append(line)
    (h.root/'build/presentation-tests.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

def boot(host=None):
    h.core.retro_reset();h.frames(90)
    if host is not None:
        for _ in range(host):h.press(7)
        h.press(8)
        if host==2:start_search_from_intro()

def snapshot():
    fields=['mode','host','completed','seconds','tick','health','misses','repairs','hits','found',
            'px','py','cursor_x','cursor_y','song_tick','song_step','music_act','count_in',
            'rhythm_phase','chart_step','cue_head','task_active','repair_task','task_progress',
            'task_cursor','task_value','task_target','task_phase','task_error','task_mistakes',
            'rng','world_seed','district','target','feedback','reaction_time','anim_tick']
    values=tuple(r(name) for name in fields)
    for name,size in [('alarm',4),('task_order',3),('task_code',4),('task_frame',2),
                      ('note_age',3),('note_live',3),('note_key',3),('score',2),('attempt_score',2)]:
        values+=tuple(r(name,i) for i in range(size))
    return values

def pause_cycle(label,panel=False):
    h.press(3)
    check(r('paused')==1 and r('art_bank')==49 and not r('hud_on'),'Dedicated pause card: '+label)
    state=snapshot();picture=hashlib.sha256(h.screen[0]).hexdigest()
    h.frames(180,[4,5,6,7])
    check(state==snapshot() and picture==hashlib.sha256(h.screen[0]).hexdigest(),'Pause ignores movement and freezes gameplay and music: '+label)
    h.press(2)
    check(r('paused')==1 and r('pause_help')==1 and state==snapshot(),'Select opens controls without consuming game state: '+label)
    h.screenshot('presentation-controls-'+label+'.png')
    h.frames(180,[8])
    check(state==snapshot(),'A held on the controls page cannot restart the attempt: '+label)
    h.press(0)
    check(r('paused')==1 and r('pause_help')==0 and state==snapshot(),'B returns from controls to pause without leaving the game: '+label)
    for _ in range(3):h.press(2);h.press(2)
    check(state==snapshot(),'Repeated help toggles preserve the saved scene: '+label)
    h.frames(30);h.audio_samples.clear();h.capture_audio=True;h.frames(60);h.capture_audio=False
    pcm=struct.unpack('<'+'h'*(len(h.audio_samples)//2),h.audio_samples)
    check(bool(pcm) and max(abs(value) for value in pcm)<64,'Paused audio settles to silence: '+label)
    h.press(3)
    check(not r('paused') and r('hud_on') and r('mode') in (1,2,3),'Start resumes the same minigame: '+label)
    if panel:check(r('task_active')==1,'Resume stays inside the same repair panel: '+label)

boot();h.screenshot('presentation-menu.png');h.frames(60,[4])
check(r('mode')==8 and r('completed')==0,'Up opens optional help without starting a timed game')
h.frames(5);pictures=[]
for host in range(3):
    check(r('mode')==8 and r('host')==host,'Help identifies selected host '+str(host))
    h.screenshot('presentation-help-'+str(host)+'.png');pictures.append(hashlib.sha256(h.screen[0]).hexdigest())
    h.press(7)
check(len(set(pictures))==3 and r('host')==0,'Help pages are distinct and right navigation wraps')
h.press(6);check(r('host')==2,'Left also wraps within help')
h.press(0);check(r('mode')==0 and r('host')==2,'B returns to the same menu selection')
for host in range(3):
    boot();h.press(4)
    for _ in range(host):h.press(7)
    h.press(8)
    check(r('mode')==(7 if host==2 else host+1),'A launches host '+str(host)+' from help')
    if host==2:start_search_from_intro()
    pause_cycle(['studio','rhythm','search'][host])
    h.press(3);h.press(0)
    check(r('mode')==0,'Pause exit returns to the portrait menu: '+str(host))

def go(x,y):
    for _ in range(500):
        px,py=r('px'),r('py')
        if px==x and py==y:return
        tx,ty=x,y
        if py<140 and ((px<128)!=(x<128)):tx,ty=(32 if px<128 else 208),144
        h.frames(1,[7 if px<tx else 6] if px!=tx else [5 if py<ty else 4])
    raise AssertionError('Could not approach repair station')

for station in range(4):
    boot(0);go(32 if station%2==0 else 208,64 if station<2 else 136)
    for _ in range(900):
        if r('alarm',station):break
        h.frames(1)
    h.press(8)
    check(r('task_active')==1 and r('repair_task')==station,'Opened actual repair panel '+str(station))
    pause_cycle('panel-'+str(station),True)
    for frame in range(600):
        if not r('task_active'):break
        h.frames(1,task_keys(frame))
    check(r('repairs')==1 and not r('task_active'),'Restored panel remains solvable: '+str(station))

boot(1);h.press(8)
for _ in range(3000):
    if r('mode')!=2:break
    head=r('cue_head')
    keys=[[8,0,6,7,4,5][r('note_key',head)]] if head<3 and r('note_age',head)==90 else []
    h.frames(1,keys)
h.frames(12)
check(r('mode')==4 and r('result_grade')==3 and r('completed')==2,'A perfect performance reaches the new result card with its earned seal')
check(r('art_bank')==49 and r('ex_on')==0 and not r('hud_on'),'Results use the dedicated slate without gameplay HUD overwrites')
h.screenshot('presentation-result-win.png');h.press(8);h.press(4);h.press(8)
check(r('mode')==8 and r('completed')==2,'Help cannot restart an already completed character')
h.press(7);h.press(3)
check(r('mode')==7 and r('completed')==2,'Start from help preserves earned seals and enters the Dany card')
start_search_from_intro();h.press(3);h.press(8)
check(r('mode')==7 and r('completed')==2,'Pause retry preserves other seals and returns to the proper intro')
h.core.retro_reset();h.frames(90);h.press(4);h.core.retro_reset();h.frames(90)
check(r('mode')==0 and not r('paused') and r('ex_on')==1,'Reset from help restores normal menu bank mapping')
h.press(8);h.press(3);h.core.retro_reset();h.frames(90)
check(r('mode')==0 and not r('paused') and r('completed')==0,'Reset from pause discards the old scene snapshot safely')
budget=json.loads((h.root/'assets/art-budget.json').read_text())
check(budget['banks_used']==50 and budget['backgrounds']['presentation']<=256 and len(h.rom)==393232,'Presentation fits the existing cartridge with one extra CHR page')
h.close()
