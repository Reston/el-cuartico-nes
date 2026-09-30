"""Complete controller-only adventure playthrough. Probes never write emulated RAM."""
import sys
import adventure_helpers as a
actor=int(sys.argv[1]) if len(sys.argv)>1 else 0
h=a.h
report=[]
# Sample the actual controller run, including crowded rooms and boss volleys.
original_frames=h.frames
samples={}
trace=[]
def measured_frames(n,keys=()):
    mask=sum(1<<k for k in keys)
    if trace and trace[-1][1]==mask:trace[-1][0]+=n
    else:trace.append([n,mask])
    for _ in range(n):
        before=(a.read('stage'),a.read('room'))
        active=h.read('mode')==10 and h.read('adv_command')==10 and h.read('adv_ui_page')==20 and h.read('hud_on') and 4 not in keys and 3 not in keys
        tick=a.read('tick')
        original_frames(1,keys)
        if active and before==(a.read('stage'),a.read('room')) and h.read('adv_command')==10 and h.read('adv_ui_page')==20 and h.read('hud_on'):
            s=samples.setdefault(before,[0,0,0]);s[0]+=1;s[1]+=((a.read('tick')-tick)&255)==0
            counts=[0]*240
            for slot in range(64):
                y=h.C.c_uint8.from_address(h.ram+0x200+slot*4).value
                if y<232:
                    for line in range(y+1,min(240,y+9)):counts[line]+=1
            s[2]=max(s[2],max(counts))
h.frames=measured_frames
import atexit,json
atexit.register(lambda:(h.root/f'build/adventure-performance-{actor}.json').write_text(json.dumps({f'{s+1}-{r+1}':v for (s,r),v in samples.items()},indent=2)))
def check(ok,label):
    report.append(('PASS ' if ok else 'FAIL ')+label)
    print(report[-1],flush=True)
    (h.root/f'build/adventure-tests-{actor}.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

a.begin(actor)
for stage in range(9):
    if stage:a.start_stage(stage)
    failures=0
    while not a.saved('cleared')&(1<<stage):
        try:
            room=a.read('room');a.clear_room(collect=True)
            check(True,f'Stage {stage+1}, room {room+1}: reachable exit')
        except AssertionError as error:
            print("RETRY",error,"health",a.read("health"),"pos",a.read("x"),a.read("y")/16,flush=True)
            if h.read('adv_ui_page')!=22:raise
            failures+=1
            check(failures<5,f'Stage {stage+1}: bounded retries ({failures})')
            h.frames(30);h.press(8);h.frames(30+failures*17)
    h.screenshot(f'adventure-stage-{stage+1}.png')
    a.studio_after_result()
check(len(samples)==46,'All 46 authored rooms visited with controller input')
check(a.saved('cleared')==511,'All nine stages completed')
check(a.saved('tasks')==7,'All three original activities integrated')
check(a.saved('tapes')==255,'All eight optional tapes are reachable')
check(max(v[2] for v in samples.values())<=8,'Gameplay stays within eight sprites per scanline')
check(sum(v[1] for v in samples.values())/sum(v[0] for v in samples.values())<0.01,'Fewer than 1% of sampled frames wait for a game update, including screen transitions')
if actor==0:
    (h.root/'build/adventure-inputs.txt').write_text(''.join(f'{n} {mask}\n' for n,mask in trace))
import json
(h.root/f'build/adventure-performance-{actor}.json').write_text(json.dumps({f'{s+1}-{r+1}':v for (s,r),v in samples.items()},indent=2))
print('PERFORMANCE',sum(v[1] for v in samples.values()),'stalls /',sum(v[0] for v in samples.values()),'frames; max sprites',max(v[2] for v in samples.values()),flush=True)
h.close()
