"""Controller-only campaign integration tests in the independent FCEUmm core."""
import itertools
import retro_harness as h
from play_helpers import repair_keys,start_search_from_intro
report=[]
def check(ok,label):
    report.append(('PASS ' if ok else 'FAIL ')+label)
    print(report[-1],flush=True)
    (h.root/'build/campaign-tests.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

def read(name,offset=0):return h.C.c_uint8.from_address(h.ram+h.labels['_'+name]+offset).value

def select(host):
    assert read('mode')==0
    for _ in range(3):
        if read('host')==host:return
        h.press(7)
    raise AssertionError('selection did not change')

def pause_check():
    mode=read('mode');h.press(3)
    before=[read(n) for n in ['seconds','px','cue_x','cursor_x','cursor_y','hits','repairs']]
    h.frames(120,[7])
    after=[read(n) for n in ['seconds','px','cue_x','cursor_x','cursor_y','hits','repairs']]
    check(read('paused')==1 and before==after,'Pause freezes minigame '+str(mode))
    h.press(3);check(read('paused')==0,'Resume minigame '+str(mode))

def toward(x,y):
    px,py=read('px'),read('py')
    if abs(px-x)>2:return 7 if px<x else 6
    if abs(py-y)>2:return 5 if py<y else 4
    return None

def repair_bot(f):return repair_keys(f)

def rhythm_bot():
    if read('cue_wait'):return []
    if read('cue_demo'):return [8]
    if 54<=read('cue_x')<=70:return [[8,0,6,7,4,5][read('cue_key')]]
    return []

def search_bot():
    if read('search_wait') or read('feedback'):return []
    if read('district')!=read('target_district'):
        d,t=read('district'),read('target_district')
        return [7 if (d&1)<(t&1) else 6] if (d&1)!=(t&1) else [5 if d<t else 4]
    target=read('target');x=read('npc_x',target);y=read('npc_y',target)+4
    if read('cursor_x')<x:return [7]
    if read('cursor_x')>x:return [6]
    if read('cursor_y')<y:return [5]
    if read('cursor_y')>y:return [4]
    return [8]


def beat(host,do_pause=False,shots=False):
    select(host);h.press(3)
    if host==2:start_search_from_intro()
    check(read('mode')==host+1,'Selected character enters its own game: '+str(host))
    if do_pause:pause_check()
    if shots:h.screenshot(['campaign-chucho.png','campaign-estefania.png','campaign-daniel.png'][host])
    seen=set();sprinted=False
    for f in range(8500):
        if read('mode') not in [1,2,3]:break
        if not read('hud_on'):
            h.frames(1)
            continue
        if host==0:
            keys=repair_bot(f);sprinted|=bool(read('dashing'))
        elif host==1:keys=rhythm_bot()
        else:
            n=read('crowd_count')
            assert sum(read('crowd',i)==0 for i in range(n))==int(read('district')==read('target_district'))
            if read('found') not in seen:
                seen.add(read('found'))
                if shots and read('seconds')>1:h.screenshot('campaign-search-'+str(read('found'))+'.png')
            keys=search_bot()
        h.frames(1,keys)
    h.frames(25)
    check(bool(read('completed')&(1<<host)),'Game objective earns its stamp: '+str(host))
    if host==0:check(read('repairs')==12 and read('seconds')>0 and sprinted,'Chucho wins at 12 live takes, before timeout, with sprint')
    if host==1:check(read('hits')==20,'Estefania wins at 20 cues')
    if host==2:check(read('found')==3 and len(seen)==3,'Daniel requires all three plaza searches')
    if read('completed')!=7:
        check(read('mode')==4 and read('last_win')==1,'Partial completion does not unlock the ending')
        h.press(3);check(read('mode')==0,'Return to free selection hub')
        if shots:h.screenshot('campaign-hub-'+str(read('completed'))+'.png')
    else:check(read('mode')==5,'Only all three stamps unlock the ending')

h.frames(90)
check(read('mode')==0 and read('completed')==0,'Boots into free-selection hub with no instruction wall')
h.screenshot('campaign-hub.png')
# Complete every permutation: each character can be first, middle or last.
for index,order in enumerate(itertools.permutations(range(3))):
    if index:h.core.retro_reset();h.frames(90)
    for host in order:beat(host,do_pause=index==0,shots=index==0)
    check(read('completed')==7,'Completion order '+str(order))
    if index==0:h.screenshot('campaign-ending.png')
    h.press(3);check(read('mode')==0 and read('completed')==0,'Explicit new episode clears stamps')

# Preserve completed contributions while abandoning and retrying other games.
beat(2)
select(0);h.press(3);h.press(3);h.press(0)
check(read('mode')==0 and read('completed')==4,'Leaving paused Chucho preserves Daniel stamp')
select(1);h.press(3);h.press(8) # finish the untimed teaching cue
for _ in range(2400):
    if read('mode')==4:break
    h.frames(1)
h.frames(25)
check(read('mode')==4 and read('last_win')==0 and read('misses')==5,'Five missed performance cues lose the attempt')
check(read('completed')==4,'A failed performance preserves other stamps')
h.screenshot('campaign-retry.png')
h.press(8)
check(read('mode')==2 and read('hits')==0 and read('completed')==4,'Retry resets only the current game')
h.press(3);h.press(0)
select(0);h.press(3)
for _ in range(3500):
    if read('mode')==4:break
    h.frames(1)
h.frames(25)
check(read('mode')==4 and read('last_win')==0 and read('health')==0,'Five missed repairs lose Chucho game')
h.press(0)
# A completed character stays marked; it cannot clear or replace its stamp.
select(2);h.press(3);check(read('mode')==0 and read('completed')==4,'Completed character remains stamped')
h.core.retro_reset();h.frames(90);select(2);h.press(3);start_search_from_intro()
first=read('previous_target')
# Deliberately select the empty corner, away from all hiding spots.
while read('cursor_x')>8:h.frames(1,[6])
while read('cursor_y')>72:h.frames(1,[4])
h.frames(1)
before=read('seconds');h.press(8)
check(read('seconds')<=before-5 and read('found')==0,'Wrong search selection deducts time without credit')
h.press(3);h.press(8);start_search_from_intro()
check(read('previous_target')!=first,'Search retry moves the hiding spot')
for _ in range(4300):
    if read('mode')==4:break
    h.frames(1)
h.frames(25)
check(read('mode')==4 and read('last_win')==0,'Search timeout loses the attempt')
check(h.audio_peak>0,'APU output is non-silent')
h.close()
report.append('ALL CAMPAIGN CHECKS PASSED')
(h.root/'build/campaign-tests.txt').write_text('\n'.join(report)+'\n')
