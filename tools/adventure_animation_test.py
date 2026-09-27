"""Controller-only regression for visible character movement and action timing.

OAM and RAM are read-only probes. The checks cover animation freezing under B,
flipped limbs, disappearing spawn sprites, and shots preceding their action.
"""
import sys
import adventure_helpers as a
h=a.h
actor=int(sys.argv[1]) if len(sys.argv)>1 else 0
report=[]
def check(ok,label):
    report.append(('PASS ' if ok else 'FAIL ')+label)
    print(report[-1],flush=True)
    (h.root/f'build/adventure-animation-tests-{actor}.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

def oam(slot,field):return h.C.c_uint8.from_address(h.ram+0x200+slot*4+field).value

def retry():
    h.press(3);h.press(5);h.press(8);h.frames(65)
    assert h.read('adv_command')==10 and a.read('room')==0

def sample(n,keys=()):
    frames=[]
    for _ in range(n):
        h.frames(1,keys)
        frames.append((oam(0,1),oam(4,1),oam(6,1),oam(0,2),oam(0,0),a.read('x'),a.read('ground'),a.read('vy')))
    return frames

a.begin(actor)
idle=sample(50)
check(all(f[4]<230 for f in idle),'Spawn protection keeps the character visible')
start=a.read('x');run=sample(24,[7])
check(a.read('x')==start+48 and len({f[2] for f in run})==6,'Six distinct leg poses accompany actual horizontal movement')
stop=sample(20)
check(len({f[2] for f in stop[3:]})==1,'Releasing movement settles the feet instead of cycling in place')
h.frames(5,[6]);sample(3)
check(all(oam(i,2)&64 for i in range(8)) and oam(0,1)==oam(1,1)+1,'Facing left mirrors both tile order and pixels')
retry();moving_action=sample(24,[7,0])
check(len({f[2] for f in moving_action})==6 and len({f[1] for f in moving_action})>=3,'Moving attacks preserve all six stride poses beneath changing arms')
retry();jump=sample(10,[8])+sample(60)
rising={f[0] for f in jump if f[7]<-25};falling={f[0] for f in jump if f[7]>30}
check(bool(rising and falling) and rising.isdisjoint(falling),'Ascending and descending jumps have different silhouettes')
land=next((i for i in range(1,len(jump)) if not jump[i-1][6] and jump[i][6]),None)
check(land is not None and jump[land+2][2]!=jump[-1][2],'Landing briefly compresses the legs before returning to idle')
retry();jump_action=sample(10,[8,0])+sample(12,[0])
check(len({f[2] for f in jump_action if not f[6]})>=2,'Airborne actions retain jump and fall leg poses')
retry()
shot_frames=[];action_frames=[]
for f in range(17):
    h.frames(1,[0] if f==0 else [])
    if any(a.read('bullets',i*6+2) and a.read('bullets',i*6+3) for i in range(3)):shot_frames.append(f)
    if oam(8,1)==128+actor*2:action_frames.append(f)
check(bool(action_frames) and action_frames[0]>=2,'The visible action follows a short anticipation')
if actor==1:
    check(bool(shot_frames) and 2<=shot_frames[0]<=4 and abs(shot_frames[0]-action_frames[0])<=1,'A projectile begins with the microphone action, never before it')
else:
    check(not shot_frames,'Melee characters do not emit an unintended projectile')
# Let the first patrol make contact without attacking it. This uses the same
# public movement route, and observes the reaction before invulnerability blink.
retry();a.clear_room();a.clear_room();h.frames(60)
original_frames=h.frames
hurt_images=[];observing=0

def unarmed_frames(n,keys=()):
    global observing
    for _ in range(n):
        health=a.read('health')
        original_frames(1,[key for key in keys if key!=0])
        if observing:
            hurt_images.append((oam(0,0),oam(0,1)))
            observing-=1
        if a.read('health')<health and not hurt_images:observing=6
h.frames=unarmed_frames
a.jump_to(1)
for _ in range(220):
    if len(hurt_images)>=6:break
    h.frames(1)
h.frames=original_frames
check(len(hurt_images)>=6 and all(y<230 and tile//8==15 for y,tile in hurt_images[:6]),'Contact damage shows a visible recoil before invulnerability blinking')
h.close()
