"""Controller navigation helpers; no emulator state is modified."""
import retro_harness as h
def read(n,i=0):return h.C.c_uint8.from_address(h.ram+h.labels['_'+n]+i).value
def district_go(wanted):
    for _ in range(1000):
        if read('mode')!=3:raise AssertionError('Left search while travelling')
        if not read('hud_on'):h.frames(1);continue
        d=read('district')
        if d==wanted:
            h.frames(15);return
        if (d&1)!=(wanted&1):key=7 if (d&1)<(wanted&1) else 6
        else:key=5 if d<wanted else 4
        h.frames(1,[key])
    raise AssertionError('District navigation timed out')
def target_area():district_go(read('target_district'))

def task_keys(f):
    t=read('repair_task');p=read('task_progress');tap=f%4<2
    if t==0:
        wanted=next(i for i in range(3) if read('task_order',i)==p)
        if read('task_cursor')!=wanted:return [5] if tap else []
        return [8] if tap else []
    if t==1:
        v,w=read('task_value'),read('task_target')
        if v!=w:return [7 if v<w else 6]
        return [8] if tap else []
    if t==2:return [8] if abs(read('task_value')-read('task_target'))<=3 and tap else []
    return [[6,7,4,5][read('task_code',p)]] if read('task_phase') and tap else []

def repair_keys(f):
    if read('task_active'):return task_keys(f)
    active=[i for i in range(4) if read('alarm',i)]
    if not active:return []
    t=min(active,key=lambda i:read('alarm',i));x=32 if t%2==0 else 208;y=64 if t<2 else 136
    px,py=read('px'),read('py')
    if py<140 and ((px<128)!=(x<128)):x,y=(32 if px<128 else 208),144
    if abs(px-x)>2:keys=[7 if px<x else 6]
    elif abs(py-y)>2:keys=[5 if py<y else 4]
    else:return [8] if f%4<2 else []
    if not read('cooldown'):keys.append(0)
    return keys


def start_search_from_intro():
    """Explicit controller confirmation of Daniel's untimed title card."""
    assert read('mode')==7, 'Daniel should first show his title card'
    h.frames(3)
    h.press(8)
    h.frames(5)
    assert read('mode')==3 and read('hud_on'), 'A should enter the first plaza'
