"""Read-only adventure probes and controller navigation for emulator tests."""
import ctypes as C
import os
os.environ['ADVENTURE_TEST_BOOT']='1'
import retro_harness as h
from play_helpers import repair_keys
FIELDS = dict(zip('stage room world health x facing ground coyote buffer attack cooldown inv tick'.split(), range(13)))
FIELDS.update(y=13,vy=15)
FIELDS.update(zip('checkpoint damaged keys tape exit_y gate_x gate_y tape_x tape_y dead hitstop'.split(),range(17,28)))
FIELDS.update(zip('boss_hp boss_tick boss_inv room_seen helped flash clue death_count'.split(),range(28,36)))
FIELDS.update(flags=36,platforms=44,enemies=64,bullets=91,boss_x=109,boss_y=110,props=111)
def read(name, index=0):
    address = h.ram + h.labels['_adv'] + FIELDS[name] + index
    if name in ('y','vy'):return C.c_int16.from_address(address).value
    return C.c_uint8.from_address(address).value

def saved(name):
    offset={'valid':0,'easy':1,'tasks':2,'tapes':3,'cleared':4,'perfect':6}[name]
    kind=C.c_uint16 if name in ('cleared','perfect') else C.c_uint8
    return kind.from_address(h.ram+h.labels['_adv_save']+offset).value

def begin(actor=0):
    h.frames(90)
    assert h.read('mode')==10
    h.press(8)  # new adventure
    h.frames(30);h.press(8);h.frames(30)  # prologue
    assert h.read('adv_ui_page')==1
    for _ in range(actor):h.press(2)
    h.press(8)  # first pitch preparation
    assert h.read('adv_ui_page')==7
    h.press(8)
    for f in range(18000):
        if h.read('mode')!=1:break
        h.frames(1,repair_keys(f))
    assert h.read('mode')==10 and saved('tasks')&1, 'Short repair should prepare the set'
    assert h.read('adv_ui_page')==2
    h.frames(30)
    h.press(8)
    h.frames(30)
    assert h.read('adv_command')==10 and read('stage')==0


def platform(i):
    return tuple(read('platforms',i*4+j) for j in range(4))

def walk(x, limit=150):
    assert h.read('adv_ui_page')!=22, 'Retry screen before walking'
    for _ in range(limit):
        if abs(read('x')-x)<=2:return
        h.frames(1,[0,7 if read('x')<x else 6])
        assert h.read('adv_command')==10, ('walk interrupted',read('stage'),read('room'),read('x'),read('y')/16,h.read('adv_ui_page'),h.read('mode'),h.read('adv_command'),read('health'))
    raise AssertionError(('walk timeout',x,read('x')))

def jump_to(i, retries=0):
    assert h.read('adv_ui_page')!=22, 'Retry screen before jumping'
    for _ in range(120):
        if read('ground'):break
        h.frames(1,[0])
    target=platform(i); tx=target[0]+target[2]//2-8
    current=next((platform(j) for j in range(5) if platform(j)[2] and read('y')//16+24==platform(j)[1] and read('x')+12>platform(j)[0] and read('x')<platform(j)[0]+platform(j)[2]),None)
    assert current, ('not grounded',read('stage'),read('room'),read('x'),read('y')/16)
    takeoff=max(current[0]+4,min(current[0]+current[2]-16,tx))
    walk(takeoff)
    for _ in range(60):
        h.frames(1,[0])
        if read('ground'):break
    h.frames(1,[0])
    airborne=False
    for f in range(220):
        target=platform(i);tx=target[0]+target[2]//2-8
        keys=[0,8]
        if abs(read('x')-tx)>2:keys.append(7 if read('x')<tx else 6)
        h.frames(1,keys)
        if h.read('adv_ui_page')==22:raise AssertionError(('jump died',read('stage'),read('room'),i))
        airborne|=not read('ground')
        if f>5 and airborne and read('ground'):
            if read('y')//16+24==target[1]:
                h.frames(1,[0]);return
            if read('y')//16+24<target[1]:
                ledge=next(platform(j) for j in range(5) if platform(j)[2] and platform(j)[1]==read('y')//16+24 and read('x')+12>platform(j)[0] and read('x')<platform(j)[0]+platform(j)[2])
                side=ledge[0]-14 if ledge[0]>target[0] else ledge[0]+ledge[2]
                walk(side)
                for _ in range(90):
                    keys=[0]
                    if read('y')//16+24>ledge[1]+4 and abs(read('x')-tx)>2:keys.append(7 if read('x')<tx else 6)
                    h.frames(1,keys)
                    if read('ground') and read('y')//16+24==target[1]:return
            if retries<3:return jump_to(i,retries+1)
            raise AssertionError(('wrong platform',read('stage'),read('room'),i,read('x'),read('y')/16,target))
    raise AssertionError(('jump timeout',i,read('x'),read('y')/16))

def clear_room(collect=False):
    old=read('room')
    if h.read('host')==0 and old==0:h.screenshot(f'adventure-world-{read("stage")}.png')
    if read('boss_hp'):
        # Approach from the left on the arena floor; duck under aerial volleys,
        # hop over the low shots, attack only during the recovery window.
        walk(112 if h.read('host')==1 and read('world')==1 else 140)
        jump_hold=0
        for f in range(2400):
            if f==125 and h.read('host')==0:h.screenshot(f'adventure-boss-{read("stage")}.png')
            if not read('boss_hp'):break
            t=read('boss_tick');keys=[0]
            target=112 if h.read('host')==1 and read('world')==1 else 140
            if read('world') in (0,4):
                if 44<=t<95:target=112 if t<68 else 140
            elif h.read('host')==1 and read('world')==1:
                danger=any(read('bullets',k*6+2) and not read('bullets',k*6+3) and read('x')-4<read('bullets',k*6)<read('x')+60 for k in range(3))
                if danger and read('ground') and not jump_hold:jump_hold=4
                if jump_hold:keys.append(8);jump_hold-=1
            elif 42<=t<73 or 80<=t<104:keys.append(8)
            if read('world') in (0,4):
                if read('x')>target+1:keys.append(6)
                elif read('x')<target-1:keys.append(7)
            h.frames(1,keys)
            if h.read('adv_ui_page')==22:raise AssertionError(('boss died',read('stage'),read('boss_hp')))
        assert not read('boss_hp'), 'Boss should be beatable during its recovery'
        walk(220);h.press(4);h.frames(30)
        assert read('room')==old+1
        return
    for i in (1,2):
        jump_to(i)
        if read('world')==3:walk(platform(i)[0]+8)
        if collect and read('tape') and i==1 and platform(4)[2]:
            jump_to(4);jump_to(1)
        if i==(1 if read('world')==2 else 2) and read('world')!=3:
            walk(read('gate_x')-10)
            h.frames(1,[7,0])
            for f in range(180):
                if read('keys') or h.read('adv_ui_page') in (10,22):break
                h.frames(1,[0]+([4] if f%8<4 else []))
            if h.read('adv_ui_page')==10:
                h.frames(30)
                for _ in range(read('clue')):h.press(5)
                h.press(8);h.frames(30)
            assert read('keys'), ('gate not activated',read('stage'),read('room'),read('x'),read('y')/16)
    jump_to(3)
    if read('world')==3:walk(platform(3)[0]+8)
    walk(220);h.press(4)
    if h.read('adv_ui_page')==21:h.frames(20);h.press(8)
    h.frames(30)
    assert read('room')==old+1, ('exit',read('stage'),old,read('keys'),read('x'),read('y')/16)


def studio_after_result():
    for _ in range(4):
        h.frames(30)
        if h.read('adv_ui_page')==1:return
        assert h.read('adv_ui_page') in (4,23,9), h.read('adv_ui_page')
        h.press(8)
    raise AssertionError('No return to studio')

def task_keys(f):
    from play_helpers import read as r
    if r('mode')==1:return repair_keys(f)
    if r('mode')==2:
        if r('cue_wait'):return []
        if r('cue_demo'):return [8]
        return [[8,0,6,7,4,5][r('cue_key')]] if 54<=r('cue_x')<=70 else []
    if r('search_wait') or r('feedback'):return []
    if r('district')!=r('target_district'):
        d,t=r('district'),r('target_district')
        return [7 if (d&1)<(t&1) else 6] if (d&1)!=(t&1) else [5 if d<t else 4]
    target=r('target');x=r('npc_x',target);y=r('npc_y',target)+4
    if r('cursor_x')!=x:return [7 if r('cursor_x')<x else 6]
    if r('cursor_y')!=y:return [5 if r('cursor_y')<y else 4]
    return [8]

def start_stage(stage):
    selected=stage//2 if stage<6 else stage-3
    while h.read('adv_ui_sel')!=selected:
        h.press(5)
        # The selection is committed only on A, so track the cursor locally.
        break
    # Caller advances one world at a time in campaign order.
    if stage<6 and h.read('adv_trial')!=(stage&1):h.press(7)
    h.press(8);h.frames(30)
    if h.read('adv_ui_page')==7:
        h.press(8)
        for f in range(18000):
            if h.read('mode')==10:break
            h.frames(1,task_keys(f))
        assert saved('tasks')&(1<<(stage//2)), ('task failed',stage,h.read('adv_activity_result'))
        h.frames(30)
    assert h.read('adv_ui_page')==2, ('intro',stage,h.read('adv_ui_page'))
    h.press(8);h.frames(30)
    assert read('stage')==stage and h.read('adv_command')==10
