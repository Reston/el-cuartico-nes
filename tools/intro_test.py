"""Controller and graphics regressions for the Dany intro and menu likenesses."""
import hashlib,json
import retro_harness as h
from play_helpers import read as r,start_search_from_intro
report=[]
def check(ok,label):
    line=('PASS ' if ok else 'FAIL ')+label;print(line,flush=True);report.append(line)
    (h.root/'build/intro-tests.txt').write_text('\n'.join(report)+'\n');assert ok,label

def boot_card(button=8):
    h.core.retro_reset();h.frames(90);h.press(7);h.press(7);h.frames(60,[button])

boot_card()
check(r('mode')==7 and r('completed')==0,'Choosing Daniel shows the title card without earning a stamp')
check(r('ex_on')==2 and r('hud_on')==0,'Title card uses static extended attributes without a gameplay HUD')
check(r('mode')==7,'Holding the launch button cannot immediately skip the card')
snapshot=tuple(r(n) for n in ['seconds','tick','found','completed','score','round_no'])
picture=hashlib.sha256(h.screen[0]).hexdigest()
h.frames(4200)
check(snapshot==tuple(r(n) for n in ['seconds','tick','found','completed','score','round_no']),'Waiting over a minute on the intro consumes no search time or progress')
check(hashlib.sha256(h.screen[0]).hexdigest()==picture,'Card stays intact through more than a minute of NMIs')
h.screenshot('dany-intro.png')
h.press(0)
check(r('mode')==0 and r('host')==2 and r('ex_on')==1,'B restores the portrait menu and keeps Daniel selected')
h.press(3);h.frames(20);h.press(3);h.frames(5)
check(r('mode')==3 and r('ex_on')==0 and r('seconds')==60 and r('misses')==0,'Start begins a fresh first round without an accidental guess')
h.press(3);h.press(8)
check(r('mode')==7 and r('found')==0,'Retry returns to the title card with search progress reset')
start_search_from_intro()
check(r('mode')==3 and r('misses')==0,'A also begins the search without consuming a guess')
# Reset from the extra PRG data bank must still find the fixed startup vectors.
boot_card(3);h.core.retro_reset();h.frames(90)
check(r('mode')==0 and r('ex_on')==1,'Reset from the card restores the normal menu and MMC5 bank mapping')
# Portrait changes must retain atomic text updates and a stable top banner.
h.screenshot('portraits.png')
raw,w,ht,pitch,fmt=h.screen;banner=raw[56*pitch:80*pitch];bad=0
for key in [7,7,7,6,6,6]*5:
    for f in range(4):
        before=r('anim_tick');h.frames(1,[key] if f==0 else [])
        bad+=((r('anim_tick')-before)%256!=1 or h.screen[0][56*pitch:80*pitch]!=banner)
check(bad==0,'Updated portraits preserve glitch-free 60 Hz character selection')
budget=json.loads((h.root/'assets/art-budget.json').read_text())
ex=(h.root/'assets/dany-intro.exram').read_bytes()
check(256<budget['backgrounds']['dany_intro']<=512 and set(v&63 for v in ex[:960])=={47,48},'Card uses two populated CHR pages within its 512-tile budget')
check(set(v>>6 for v in ex[:960])=={0,1,2,3},'Card keeps separate blue, red, grayscale and stone subpalettes')
check(budget['banks_used']==50 and len(h.rom)==393232,'Intro fits the existing MMC5 cartridge size')
nt=(h.root/'assets/title.exram').read_bytes()
check([nt[21*32+x]>>6 for x in (4,12,20)]==[3,2,0],'Menu clothing uses Chucho green, Estefania jacket and Daniel white palettes')
h.close()
