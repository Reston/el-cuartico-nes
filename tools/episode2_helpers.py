"""Controller helpers shared by the two-episode campaign checks."""
import retro_harness as h
from play_helpers import read as r,repair_keys,task_keys,start_from_intro
KEYS=[8,0,6,7,4,5]

def select(host):
    assert r('mode')==0
    for _ in range(3):
        if r('host')==host:return
        h.press(7)
    raise AssertionError('Host selection stalled')

def launch(host):
    select(host);h.press(8)
    if r('mode')==9:h.press(8)
    if r('mode')==7:start_from_intro()
    assert r('mode')==host+1
    for _ in range(120):
        if r('hud_on'):break
        h.frames(1)
    assert r('hud_on');h.frames(5)

def rhythm_keys():
    if r('cue_demo'):return [8]
    if r('hold_slot')<3:return [KEYS[r('note_key',r('hold_slot'))]]
    i=r('cue_head')
    return [KEYS[r('note_key',i)]] if i<3 and r('note_age',i)==90 else []

def cursor_keys(x,y):
    if r('cursor_x')!=x:return [7 if r('cursor_x')<x else 6]
    if r('cursor_y')!=y:return [5 if r('cursor_y')<y else 4]
    return [8]

def area_keys(wanted):
    d=r('district')
    if d==wanted:return None
    return [7 if d%2<wanted%2 else 6] if d%2!=wanted%2 else [5 if d<wanted else 4]

def search_keys(props=False):
    if r('search_wait') or r('feedback'):return []
    if props and r('episode') and r('prop_mask')!=3:
        i=0 if not r('prop_mask')&1 else 1
        return area_keys(r('prop_area',i)) or cursor_keys(r('prop_x',i),80)
    return area_keys(r('target_district')) or cursor_keys(r('npc_x',r('target')),r('npc_y',r('target'))+4)

def linked_keys(f):
    if r('task_active'):return task_keys(f)
    active=[i for i in range(4) if r('alarm',i)]
    if not active:return []
    # Exercise both valid camera/mixer orders across the three broadcasts.
    t=(2 if (r('repairs')//4)%2 else 1) if 1 in active and 2 in active else active[0]
    x,y=(32 if t%2==0 else 208),(64 if t<2 else 136)
    px,py=r('px'),r('py')
    if py<140 and ((px<128)!=(x<128)):x,y=(32 if px<128 else 208),144
    if abs(px-x)>2:keys=[7 if px<x else 6]
    elif abs(py-y)>2:keys=[5 if py<y else 4]
    else:return [8] if f%4<2 else []
    if not r('cooldown'):keys.append(0)
    return keys

def game_keys(host,f,props=False):
    if host==0:return linked_keys(f) if r('episode') else repair_keys(f)
    if host==1:return rhythm_keys()
    return search_keys(props)

def complete_current(host,props=False):
    for f in range(18000):
        if r('mode') not in (1,2,3):break
        h.frames(1,game_keys(host,f,props) if r('hud_on') else [])
    h.frames(20)
    assert r('completed')&(1<<host), ('Failed to complete',r('episode'),host,r('mode'),r('misses'),r('seconds'))

def complete_episode(order=(0,1,2),props=False):
    for host in order:
        launch(host);complete_current(host,props)
        if r('mode')==4:h.press(8)
    assert r('mode')==5 and r('completed')==7
