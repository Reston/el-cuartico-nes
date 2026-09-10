"""MMC5-specific graphics, frame-pacing, magnifier and reset checks."""
import hashlib,json
import retro_harness as h
from play_helpers import start_search_from_intro
report=[]
def r(n,i=0):return h.C.c_uint8.from_address(h.ram+h.labels['_'+n]+i).value
def check(ok,msg):
    line=('PASS ' if ok else 'FAIL ')+msg;print(line,flush=True);report.append(line)
    (h.root/'build/mmc5-tests.txt').write_text('\n'.join(report)+'\n');assert ok,msg
def boot(host=None):
    h.core.retro_reset();h.frames(90)
    if host is not None:
        for _ in range(host):h.press(7)
        h.press(3)
        if host==2:start_search_from_intro()
def sprite_peak():
    ys=[h.C.c_uint8.from_address(h.ram+0x200+i*4).value for i in range(64)]
    return max(sum(y<240 and y+1<=row<=y+8 for y in ys) for row in range(240))
def steady(n=128,keys=()):
    banks=set();visuals=set();a=r('anim_tick');f=r('frame')
    for i in range(n):
        h.frames(1,keys);banks.add(r('art_bank'))
        visuals.add(hashlib.sha256(h.screen[0]).hexdigest())
    return (r('anim_tick')-a)%256,(r('frame')-f)%256,banks,visuals
budget=json.loads((h.root/'assets/art-budget.json').read_text())
check(budget['banks_used']==50 and budget['chr_bytes']==262144,'50 populated graphics banks fit 256 KiB CHR ROM')
nt=(h.root/'assets/title.nam').read_bytes()
ex=(h.root/'assets/title.exram').read_bytes()
check(set(v&63 for v in ex[:960])=={0,26},'Portrait screen uses two simultaneous 4 KiB CHR pages')
check(ex[14*32+4]>>6==0 and ex[15*32+4]>>6==1,'Adjacent 8x8 cells in one 16x16 quadrant use distinct text/skin palettes')
check(budget['backgrounds']['title']>256,'Portrait art exceeds the old single-page tile limit')
check(budget['sprite_tiles']==256,'Larger repairer frames fit the normal 256-tile sprite page')
# True Daniel remains visually unique in both tiny and detailed face sets.
chrdata=h.rom[16+131072:]
small=[chrdata[12*4096+(220+i*6)*16:12*4096+(224+i*6)*16] for i in range(6)]
large=[chrdata[25*4096+(64+i*16)*16:25*4096+(80+i*16)*16] for i in range(6)]
check(len(set(small))==len(set(large))==6,'All six plaza faces and lens faces remain visually distinct')
check(chrdata[46*4096+24*16:46*4096+28*16]==small[0] and chrdata[25*4096+24*16:25*4096+28*16]==small[0], 'Reference portrait matches Daniel with and without the lens')
for host,base,name in [(None,0,'hub'),(0,4,'studio'),(1,8,'stage'),(2,12,'plaza')]:
    boot(host);h.frames(20)
    check(r('ex_on')==int(host is None),'Extended portrait mode is selected only on the hub: '+name)
    dt,df,banks,visuals=steady()
    check(dt==df==128,'One game update per NTSC frame: '+name)
    check(banks==set(range(base,base+4)),'All four background frames selected: '+name)
    check(len(visuals)>1,'Animated pixels change: '+name)
    h.screenshot('mmc5-'+name+'.png')
boot(0)
dt,df,_,_=steady(128,[0,6])
check(dt==df==128,'Larger Chucho keeps one update per frame while moving and sprinting')
# Stress the larger performer, moving badges and hit feedback together.
boot(1);h.press(8);bad_frames=0;peak=0
for i in range(1050):
    head=r('cue_head');keys=[]
    if not r('count_in') and head<3 and 87<=r('note_age',head)<=90:
        keys=[[8,0,6,7,4,5][r('note_key',head)]]
    before=r('anim_tick');h.frames(1,keys)
    bad_frames+=((r('anim_tick')-before)%256!=1)
    peak=max(peak,sprite_peak())
    if r('judgement') and r('feedback')==12:h.screenshot('mmc5-perfect.png')
check(bad_frames==0,'No dropped game updates during active rhythm/feedback stress')
check(peak<=8,'Large performer and badges respect eight sprites per scanline')
check(r('perfects')>10 and r('misses')==0,'Tight beat hits earn perfect feedback without altering chart timing')
# Holding B inspects a face, does not answer or spend search time penalties.
boot(2);t=r('target')
while r('cursor_x')!=r('npc_x',t):h.frames(1,[7 if r('cursor_x')<r('npc_x',t) else 6])
while r('cursor_y')!=r('npc_y',t)+4:h.frames(1,[5 if r('cursor_y')<r('npc_y',t)+4 else 4])
h.frames(2);before=r('seconds');h.frames(6,[0])
check(r('zoom_npc')==t and r('sprite_bank')==100,'B selects the magnifier graphics bank over a person')
check(r('found')==0 and before-r('seconds')<=1,'Inspecting does not guess or apply a wrong-answer penalty')
h.screenshot('mmc5-magnifier.png')
dt,df,_,_=steady(120,[0]);check(dt==df==120,'Magnifier runs at one update per NTSC frame')
check(sprite_peak()<=8,'Magnifier respects normal sprite limits')
h.frames(3);check(r('sprite_bank')==184,'Releasing B restores the dedicated search sprite bank')
h.press(8);h.frames(55);check(r('found')==1 and r('round_no')==1,'A still confirms the inspected target')
check(16<=r('art_bank')<=19,'Second search selects the market art banks')
h.press(3);paused=(r('art_bank'),r('anim_tick'),r('song_step'),r('song_tick'));h.frames(80)
check(paused==(r('art_bank'),r('anim_tick'),r('song_step'),r('song_tick')),'Pause freezes scene animation and music')
h.press(0);check(r('mode')==0 and r('sprite_bank')==96,'Leaving search restores the hub and shared sprites')
boot();check(r('mode')==0 and r('completed')==0,'MMC5 reset boots from its fixed PRG bank')
check(r('ex_on')==1,'Reset restores extended portrait palettes after gameplay')
h.close();report.append('ALL MMC5 CHECKS PASSED')
(h.root/'build/mmc5-tests.txt').write_text('\n'.join(report)+'\n')
