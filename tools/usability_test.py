"""Controller and video regressions for intro cards, atomic help, exits and finales."""
import hashlib,json
import retro_harness as h
from play_helpers import read as r,start_from_intro,district_go
from episode2_helpers import launch,complete_episode,rhythm_keys,search_keys
report=[]

def check(ok,label):
    line=('PASS ' if ok else 'FAIL ')+label;print(line,flush=True);report.append(line)
    (h.root/'build/usability-tests.txt').write_text('\n'.join(report)+'\n');assert ok,label

def boot():h.core.retro_reset();h.frames(90)
def picture():return hashlib.sha256(h.screen[0]).digest()
def snapshot():
    return tuple(r(n,i) for n in ('seconds','tick','completed','found','hits','repairs','score','attempt_score') for i in range(2 if 'score' in n else 1))
def pixel(x,y):
    raw,w,ht,pitch,fmt=h.screen;size=4 if fmt==1 else 2
    return raw[y*pitch+x*size:y*pitch+(x+1)*size]

cards=[]
for host in range(3):
    boot()
    for _ in range(host):h.press(7)
    h.frames(60,[8]);h.frames(4)
    check(r('mode')==7 and r('ex_on')==2 and not r('hud_on'),'Holding launch waits on host '+str(host)+' title card')
    state,view=snapshot(),picture();h.frames(4200)
    check(state==snapshot() and picture()==view,'Host '+str(host)+' card stays intact and untimed for over a minute')
    cards.append(view);h.screenshot(['chucho-intro.png','estefania-intro.png','dany-intro.png'][host])
    h.press(0)
    check(r('mode')==0 and r('host')==host and r('ex_on')==1,'B returns to the same portrait from card '+str(host))
    h.frames(60,[3]);h.frames(3);check(r('mode')==7,'Holding Start cannot skip host '+str(host)+' card');h.press(3)
    check(r('mode')==host+1 and not r('paused') and not r('misses') and not r('hits'),'Fresh Start begins only after confirming card '+str(host))
    h.press(3);h.press(8)
    check(r('mode')==7 and not r('paused'),'Retry opens host '+str(host)+' card')
    start_from_intro()
    check(r('mode')==host+1 and not r('misses'),'A confirms host '+str(host)+' without accidental gameplay input')
    h.press(3);h.press(8);h.core.retro_reset();h.frames(90)
    check(r('mode')==0 and r('ex_on')==1 and not r('completed'),'Reset from host '+str(host)+' card restores the fixed startup bank')
check(len(set(cards))==3,'All three characters have distinct illustrated title cards')
budget=json.loads((h.root/'assets/art-budget.json').read_text())
check(budget['banks_used']==54 and len(h.rom)==393232,'New posters fit the unchanged cartridge size')


def help_switches(episode):
    h.press(4);views=set()
    for host in range(3):
        views.add(picture());h.screenshot('usability-help-e'+str(episode)+'-'+str(r('host'))+'.png');h.press(7)
    bad=stalls=0
    for key in [7,7,7,6,6,6,2,2,2]*5:
        for f in range(4):
            before=r('anim_tick');h.frames(1,[key] if f==0 else [])
            bad+=picture() not in views
            stalls+=(r('anim_tick')-before)%256!=1
    check(len(views)==3 and not bad,'Episode '+str(episode+1)+' help always shows one complete page during rapid switching')
    check(not stalls and not r('help_dirty'),'Episode '+str(episode+1)+' help switches at 60 Hz with no unfinished upload')
    h.press(0);check(r('mode')==0,'Help switching returns safely to the menu')


def finale(episode):
    launch(1);goal=49 if episode else 20
    missed=False;shot=False;final_paused=False;outro_frames=0;last_spawn=-1;seen_acts=set();bad=stalls=0
    for f in range(16000):
        if r('mode')!=2:break
        if r('hud_on') and not r('cue_demo') and not r('count_in'):
            active=sum(r('note_live',i) for i in range(3));act=r('music_act');seen_acts.add(act)
            limit=([7,13,20],[17,33,49])[episode][act]
            bad+=r('hits')+active>limit
            if act==2 and any(r('note_live',i) and r('note_age',i)==0 for i in range(3)):last_spawn=f
            if r('rhythm_outro'):outro_frames+=1
        keys=rhythm_keys()
        head=r('cue_head')
        if episode and not final_paused and r('hits')==goal-1 and r('hold_slot')<3:
            h.press(3);frozen=tuple(r(n) for n in ('hold_left','hits','misses','song_step','song_tick','rhythm_phase'))
            h.press(2);h.press(0);h.press(3)
            status=bytes(r('status_row',i) for i in range(32)).decode('ascii')
            check(r('hold_resume') and status.strip()=='RETOMA EL BOTON PARA SEGUIR','Final held-note pause shows the re-grip instruction above the outro')
            h.frames(120)
            check(frozen==tuple(r(n) for n in ('hold_left','hits','misses','song_step','song_tick','rhythm_phase')),'The last held note waits without consuming its duration or music clock')
            final_paused=True
            h.frames(1,rhythm_keys());h.frames(1,rhythm_keys())
            keys=[[8,0,6,7,4,5][(r('note_key',r('hold_slot'))+1)%6]];missed=True
        elif not missed and r('hits')==goal-1 and head<3 and r('note_age',head)==90 and not r('note_hold',head):
            keys=[[8,0,6,7,4,5][(r('note_key',head)+1)%6]];missed=True
        before=r('anim_tick');h.frames(1,keys)
        if r('mode')==2 and r('hud_on'):stalls+=(r('anim_tick')-before)%256!=1
        if not shot and r('hits')==goal-1 and r('rhythm_outro') and head<3 and 30<r('note_age',head)<80:
            h.screenshot('usability-last-note-e'+str(episode)+'.png');shot=True
    h.frames(20)
    check(not bad and seen_acts=={0,1,2},'Episode '+str(episode+1)+' stops cue spawning before each act has enough notes to finish')
    check(missed and r('hits')==goal and r('misses')==1 and r('completed')==2,'Missing the final cue schedules a replacement and still allows episode '+str(episode+1)+' victory')
    check(outro_frames>=80 and f-last_spawn>=82 and not any(r('note_live',i) for i in range(3)),'Episode '+str(episode+1)+' ends with an empty lane after the final cue has arrived')
    check(not stalls,'Final-note scheduling preserves one update per frame in episode '+str(episode+1))
    h.press(8)


def navigation(episode):
    launch(2)
    for world in range(3):
        check(r('round_no')==world,'Reached search world '+str(world+1)+' in episode '+str(episode+1))
        for area in range(1<<world):
            district_go(area)
            # Centre the cursor so it cannot cover any arrow while sampling pixels.
            for _ in range(250):
                x,y=r('cursor_x'),r('cursor_y')
                if (x,y)==(120,184):break
                h.frames(1,[7 if x<120 else 6] if x!=120 else [5 if y<184 else 4])
            h.frames(3)
            if world:
                observed=(pixel(2,143)!=pixel(2,134),pixel(253,143)!=pixel(253,134),pixel(127,64)!=pixel(116,64),pixel(127,223)!=pixel(116,223))
                expected=(bool(area&1),not bool(area&1),area>=2,world==2 and area<2)
                check(observed==expected,'Visible exit arrows match connected areas: episode '+str(episode+1)+' world '+str(world+1)+' area '+str(area+1))
                clear=all(pixel(x,y)==pixel(x,100) for x in (1,254) for y in range(96,216))
                check(clear,'Border clearance stays free of crowds and decoration in area '+str(area+1))
                if episode==0:h.screenshot('usability-map-'+str(world)+'-'+str(area)+'.png')
        for f in range(1800):
            if r('mode')!=3 or (r('round_no')!=world and r('hud_on')):break
            h.frames(1,search_keys() if r('hud_on') else [])
        h.frames(10)
    check(r('found')==3 and r('completed')==6,'Arrow-guided exploration completes all three worlds without losing the rhythm seal')

for episode in range(2):
    boot()
    if episode:complete_episode();h.press(8)
    help_switches(episode);finale(episode);navigation(episode)
h.close()
