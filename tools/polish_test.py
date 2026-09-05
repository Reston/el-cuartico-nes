"""Controller-only regressions for v0.7 feedback, streaks and plaza selection."""
import hashlib
import retro_harness as h
from play_helpers import target_area,task_keys
report=[]
def r(n,i=0):return h.C.c_uint8.from_address(h.ram+h.labels['_'+n]+i).value
def word(n):return r(n)+256*r(n,1)
def hud():return ''.join(chr(r('hud',i)) for i in range(32))
def check(ok,msg):
    line=('PASS ' if ok else 'FAIL ')+msg;print(line,flush=True);report.append(line)
    (h.root/'build/polish-tests.txt').write_text('\n'.join(report)+'\n');assert ok,msg
def boot(host=None):
    h.core.retro_reset();h.frames(90)
    if host is not None:
        for _ in range(host):h.press(7)
        h.press(3)
def pulse(k):h.frames(1,[k]);h.frames(1)
def go(x,y,who='cursor'):
    xn,yn=('px','py') if who=='repair' else ('cursor_x','cursor_y')
    for _ in range(500):
        if r(xn)==x and r(yn)==y:return
        keys=[7 if r(xn)<x else 6] if r(xn)!=x else [5 if r(yn)<y else 4]
        # Inspection allows the odd-pixel target positions as well.
        if who=='cursor' and (abs(r(xn)-x)==1 or abs(r(yn)-y)==1):keys+=[0]
        h.frames(1,keys)
    raise AssertionError('navigation failed')
def peak():
    ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
    return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
# The portrait animation includes real pixel changes, not just register writes.
boot();images={}
for _ in range(128):
    h.frames(1);images.setdefault(r('art_bank'),set()).add(hashlib.sha256(h.screen[0]).hexdigest())
check(set(images)=={0,1,2,3} and len(set.union(*images.values()))>=4,'Three short portrait blinks appear in emulator output')
h.screenshot('polish-hub.png')
# Chucho: carry status, multiplier and hearts are real state, not decorations.
boot(0);check('EN VIVO' in hud() and r('alarm',0)>0 and r('alarm',1)>0,'Live studio begins with two overlapping requests')
go(32,144,'repair');go(32,64,'repair');pulse(8)
check(r('task_active')==1 and r('repairs')==0,'Interacting with a fault opens its repair panel without free credit')
for f in range(240):
    if not r('task_active') and r('hud_on'):break
    h.frames(1,task_keys(f) if r('hud_on') else [])
check(r('repairs')==1 and r('combo')==2,'Completing the cable puzzle earns a take and streak')
h.frames(3);h.screenshot('polish-repair.png')
check(peak()<=8,'Studio action feedback fits sprite scanline limits')
bad=0;max_sprites=0
for i in range(600):
    before=r('anim_tick');h.frames(1,[5 if (i//60)%2 else 4])
    bad+=((r('anim_tick')-before)%256!=1);max_sprites=max(max_sprites,peak())
check(bad==0 and max_sprites<=8,'Studio movement and overlapping station cues stay within frame and sprite budgets')
boot(0)
for _ in range(1000):
    h.frames(1)
    if r('health')==4:break
h.frames(2)
check(r('health')==4 and r('combo')==1,'An expired request removes one heart and resets the streak')
hearts=[h.C.c_uint8.from_address(h.ram+0x201+i*4).value for i in range(64) if h.C.c_uint8.from_address(h.ram+0x200+i*4).value==208]
check(hearts.count(238)==4 and hearts.count(239)==1,'Displayed hearts match remaining health')
# Rhythm: the practice hit does not grant a streak or perfect bonus.
boot(1);pulse(8);check(r('rhythm_chain')==0 and word('attempt_score')==100,'Practice input awards no streak bonus')
def hit_next(correct=True):
    for _ in range(360):
        if r('mode')!=2:return
        head=r('cue_head')
        if not r('count_in') and head<3 and r('note_age',head)==90:
            key=r('note_key',head);pulse([8,0,6,7,4,5][key if correct else (key+1)%6]);return
        h.frames(1)
    raise AssertionError('note did not arrive')
for _ in range(5):hit_next()
check(r('rhythm_chain')==5 and r('peak_chain')==5 and word('attempt_score')==950,'Five consecutive chart hits award exactly one 100-point streak bonus')
check(r('cheer')>0 and 'X05' in hud(),'Streak feedback and live HUD counter appear')
h.screenshot('polish-streak.png')
pulse(3);frozen=(r('cheer'),r('rhythm_chain'),r('song_tick'),r('song_step'));h.frames(75)
check(frozen==(r('cheer'),r('rhythm_chain'),r('song_tick'),r('song_step')),'Pause freezes streak celebration and music together')
pulse(3);hit_next(False)
check(r('rhythm_chain')==0 and r('peak_chain')==5 and r('misses')==1 and word('attempt_score')==950,'A wrong cue clears the live streak while preserving earned points')
while r('mode')==2:hit_next()
check(r('hits')==20 and r('mode')==4 and r('result_grade')==2,'A successful run with one miss receives two result medals')
h.frames(3);h.screenshot('polish-result.png')
pulse(3);h.press(7);h.press(3)
check(r('mode')==3,'Result screen continues through normal character selection')
# Find an actual overlap where the old A rule accepted Daniel under a decoy.
def candidates():
    return [(r('npc_x',i),r('npc_y',i)+4) for i in range(r('crowd_count'))]
def nearest(coords,x,y):
    choices=[(abs(x-a)+abs(y-b),i) for i,(a,b) in enumerate(coords) if abs(x-a)<=10 and abs(y-b)<=14]
    return min(choices)[1] if choices else 255
boot(2);overlap=None
for _ in range(10):
    coords=candidates();tx,ty=coords[r('target')]
    for y in range(max(72,ty-14),min(204,ty+14)+1,2):
        for x in range(max(8,tx-10),min(232,tx+10)+1,2):
            n=nearest(coords,x,y)
            if n!=r('target') and n<24:overlap=(x,y,n);break
        if overlap:break
    if overlap:break
    pulse(3);h.press(8)
check(overlap is not None,'Fixture contains overlapping target and decoy selection areas')
x,y,n=overlap;go(x,y);h.frames(3,[0])
check(r('hover_npc')==n and r('zoom_npc')==n,'Magnifier chooses the nearest decoy in an overlapping area')
before=r('seconds');old_found=r('found');pulse(8)
check(r('found')==old_found and r('misses')==1 and 5<=before-r('seconds')<=6,'A selects the displayed decoy and applies the wrong-answer penalty')
anchor=(r('feedback_x'),r('feedback_y'));h.frames(4,[7])
check(anchor==(r('feedback_x'),r('feedback_y')),'Penalty popup stays over the guessed location when the cursor moves')
h.screenshot('polish-search-penalty.png')
# Precision movement, odd coordinates and clamps all remain reachable.
x=r('cursor_x');h.frames(1,[0,6]);check(r('cursor_x')==x-1,'Holding B provides one-pixel precision movement')
x=r('cursor_x');h.frames(1,[6]);check(r('cursor_x')==x-2,'Normal cursor movement remains two pixels')
h.frames(250,[0,7]);check(r('cursor_x')==232,'Precision cursor clamps at the right boundary')
h.frames(1,[0,6]);h.frames(1,[7]);check(r('cursor_x')==232,'Normal movement clamps correctly after an odd-pixel inspection position')
# The exact center always identifies Daniel, even among 20 people.
for scene in range(3):
    h.frames(35);target_area();go(r('npc_x',r('target')),r('npc_y',r('target'))+4);h.frames(3,[0])
    check(r('hover_npc')==r('target')==r('zoom_npc'),'Lens and selection agree on Daniel in search '+str(scene+1))
    if scene==2:
        a=r('anim_tick');f=r('frame');h.frames(128,[0,6,4])
        check((r('anim_tick')-a)%256==128 and (r('frame')-f)%256==128,'Moving inspection cursor among 20 people keeps one update per frame')
        go(r('npc_x',r('target')),r('npc_y',r('target'))+4);h.frames(3,[0]);h.screenshot('polish-search.png')
    pulse(8);h.frames(50)
check(r('found')==3 and r('completed')==4,'Consistent selection still completes all three searches')
# A correct selection owns the final second; the round transition freezes time.
boot(2);go(r('npc_x',r('target')),r('npc_y',r('target'))+4)
for _ in range(3700):
    if r('seconds')==1 and r('tick')==59:break
    h.frames(1)
check(r('seconds')==1 and r('tick')==59,'Reached the final timer frame through normal play')
pulse(8)
check(r('mode')==3 and r('found')==1 and r('search_wait')>0,'Finding Daniel on the last timer frame wins the round')
for _ in range(100):
    h.frames(1)
    if r('round_no')==1 and r('hud_on'):break
check(r('mode')==3 and r('round_no')==1 and r('seconds')==85,'Last-moment success advances into a fresh timed round')
h.close();report.append('ALL POLISH CHECKS PASSED')
(h.root/'build/polish-tests.txt').write_text('\n'.join(report)+'\n')
