"""Chapter regressions through the public password UI and controller input only.
No writes to emulated RAM, registers or emulator states.
"""
import adventure_helpers as a
h=a.h
report=[]
def check(ok,label):
    report.append(('PASS ' if ok else 'FAIL ')+label)
    print(report[-1],flush=True)
    (h.root/'build/adventure-chapter-tests.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

def load(cleared,tasks):
    h.core.retro_reset();h.frames(90);h.press(5);h.press(8);h.frames(30)
    assert h.read('adv_ui_page')==5
    v=1|(cleared<<4)|(tasks<<30);crc=0xffff
    for byte in v.to_bytes(6,'little'):
        crc^=byte<<8
        for _ in range(8):crc=((crc<<1)^0x1021 if crc&0x8000 else crc<<1)&65535
    v|=crc<<44
    for i in range(12):
        current=h.C.c_uint8.from_address(h.ram+h.labels['_adv_code']+i).value
        delta=(((v>>(i*5))&31)-current)&31
        for _ in range(min(delta,32-delta)):h.press(4 if delta<=16 else 5)
        if i<11:h.press(7)
    h.press(8);h.frames(30)
    assert h.read('adv_ui_page')==1

def retry():
    h.press(3);h.press(5);h.press(8);h.frames(60)

def routes():
    a.walk(34);h.press(4);h.frames(10)
    assert h.read('adv_ui_page')==12

def pick(i):
    routes()
    for _ in range(i):h.press(5)
    h.press(8);h.frames(30)

retry_count=0
def finish_room():
    global retry_count
    for attempt in range(4):
        try:a.clear_room(collect=True);return
        except AssertionError as error:
            print("CHAPTER RETRY",error,"health",a.read("health"),"room",a.read("room"),flush=True)
            if h.read('adv_ui_page')!=22:raise
            retry_count+=1
            assert retry_count<12, "Too many chapter retries"
            h.press(8);h.frames(30+retry_count*17)
    raise AssertionError('Chapter room failed after retries')

load(7,3);a.start_stage(3)
check(a.read('platforms',3*4+2)==0 and a.read('props')==0,'Rumor bridge starts hidden until all repeaters stop')
h.screenshot('chapters-rumor-before.png')
h.press(4);h.frames(15)
check(not a.read('props') and not a.read('keys'),'Repeaters require an action instead of the generic Up interaction')
a.relay_at(0)
check(a.read('props')==1 and not a.read('keys') and a.platform(3)[2]==0,'First repeater alone does not unlock the bridge')
retry()
check(a.read('props')==1 and not a.read('keys'),'Checkpoint retry preserves silenced repeaters without prematurely unlocking the room')
a.jump_to(1);a.relay_at(1)
check(a.read('props')==3 and a.platform(3)[2]==0,'Second repeater still leaves the exit locked')
a.jump_to(2);a.relay_at(2)
check(a.read('props')==7 and a.read('keys') and a.platform(3)[2]>0,'Third repeater reveals a solid, usable bridge')
h.screenshot('chapters-rumor-after.png')
a.jump_to(3);a.walk(220);h.press(4);h.frames(30)
check(a.read('room')==1,'Revealed bridge leads to the next room')

load(15,7)
# Move the studio cursor from first to third idea, then let start_stage commit it.
h.press(5);a.start_stage(4)
h.screenshot('chapters-plaza.png')
h.press(2);h.frames(30)
state=[a.read(n) for n in ('x','y','health','room','tick')]+[h.read('song_step'),h.read('song_tick')]
h.frames(180,[7])
check(state==[a.read(n) for n in ('x','y','health','room','tick')]+[h.read('song_step'),h.read('song_tick')],'Map and notebook freeze simulation and music')
h.screenshot('chapters-book-empty.png');h.press(2);h.frames(20)
routes();position=(a.read('x'),a.read('y'))
actor=h.read('host');h.press(2)
check(h.read('host')==(actor+1)%3,'Safe plaza allows changing actor')
h.press(2);h.press(2)
for _ in range(3):h.press(5)
h.press(8);h.frames(30)
check(h.read('adv_ui_page')==12 and a.read('room')==0,'Final path stays locked before collecting the three clues')
h.press(0);h.frames(10)
check(position==(a.read('x'),a.read('y')),'Cancel route selection returns to the same plaza position')
pick(2)
check(a.read('room')==9,'Player can visit the third clue route first')
h.press(5);h.frames(20)
check(a.read('room')==0 and a.read('flags',9)&128,'Returning to plaza preserves explored rooms')
for route in (2,0,1):
    pick(route)
    for _ in range(20):
        if a.read("room")==0:break
        finish_room()
    check(a.read('room')==0 and a.read('flags',(route+1)*4)&1,f'Conversation records clue {route+1} and returns to plaza')
    retry()
    check(a.read('flags',(route+1)*4)&1,f'Clue {route+1} survives checkpoint retry')
h.press(2);h.frames(30);h.screenshot('chapters-book-complete.png');h.press(2);h.frames(30)
routes();h.screenshot('chapters-routes-complete.png');h.press(0);h.frames(30)
pick(3)
check(a.read('room')==13,'All three learned clues unlock the final route')
while not a.saved("cleared")&16:finish_room()
check(a.saved('cleared')&16,'Nonlinear first mystery chapter completes normally')
a.studio_after_result();a.start_stage(5)
# Exercise a wrong answer and nested notebook using the actual chapter interaction.
original_choose=a.choose_clue
question_tested=False
def checked_choice():
    global question_tested
    if not question_tested:
        h.frames(10)
        health=a.read('health');clock=a.read('tick');wanted=a.read('clue')
        for _ in range((wanted+1)%3):h.press(5)
        h.press(8);h.frames(90)
        check(h.read('adv_ui_page')==10 and a.read('health')==health and a.read('tick')==clock,'Wrong clue answers give feedback without damage or a timer')
        h.press(2);h.frames(30);h.screenshot('chapters-book-in-puzzle.png');h.press(0);h.frames(30)
        check(h.read('adv_ui_page')==10 and a.read('health')==health,'Notebook returns to the same unsolved question')
        h.press(0);h.frames(30)
        check(not a.read('keys'),'Cancelling a question does not open its gate')
        h.press(4);h.frames(10)
        assert h.read('adv_ui_page')==10
        question_tested=True
    original_choose()
a.choose_clue=checked_choice
while a.read('room')!=15:finish_room()
check(question_tested,'Second mystery chapter applies the vocabulary learned in its first half')
a.walk(152)
for _ in range(150):
    h.frames(1,[0])
    if h.read('adv_ui_page')==22:break
check(a.read('boss_hp')==3,'Guardian seals cannot be bypassed by repeated attacks')
retry();h.screenshot('chapters-guardian.png');finish_room()
check(a.read('boss_marks')==7 and a.saved('cleared')&32,'Guardian is completed by all three learned symbols')
a.studio_after_result()
check(h.read('adv_ui_page')==1,'Guardian ending returns safely to the studio')
# A retry must never turn a partially collected supermarket list into an open exit.
load(63,7)
h.press(5);h.press(5);a.start_stage(6)
a.jump_to(1);a.walk(a.platform(1)[0]+8)
check(a.read('props')==1 and not a.read('keys'),'Supermarket needs all three objects before opening its exit')
retry()
check(not a.read('keys') and not a.read('flags',0)&1,'Retry cannot bypass an unfinished supermarket list')
finish_room()
check(a.read('room')==1,'Supermarket remains completable after retry')
retry()
check(a.read('room')==0 and a.read('keys') and a.read('props')==7,'A completed supermarket list stays completed after retry')
h.close()
