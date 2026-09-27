"""Input-only tests of pause, recovery, password validation, skills and classic isolation."""
import ctypes as C
import adventure_helpers as a
h=a.h
report=[]
def check(ok,label):
    report.append(('PASS ' if ok else 'FAIL ')+label);print(report[-1],flush=True)
    (h.root/'build/adventure-polish-tests.txt').write_text('\n'.join(report)+'\n')
    assert ok,label

def code():return [C.c_uint8.from_address(h.ram+h.labels['_adv_code']+i).value for i in range(12)]
def pause_option(i):
    h.press(3)
    for _ in range(i):h.press(5)
    h.press(8);h.frames(30)

def password_bytes(cleared=0,perfect=0,tapes=0,tasks=0,easy=0):
    # Independent reference encoder, used to exercise the public password form.
    v=1|(cleared<<4)|(perfect<<13)|(tapes<<22)|(tasks<<30)|(easy<<33)
    crc=0xffff
    for byte in v.to_bytes(6,'little'):
        crc^=byte<<8
        for _ in range(8):crc=((crc<<1)^0x1021 if crc&0x8000 else crc<<1)&65535
    v|=crc<<44
    return [(v>>(5*i))&31 for i in range(12)]

def enter_code(wanted):
    for i,value in enumerate(wanted):
        delta=(value-code()[i])&31
        for _ in range(min(delta,32-delta)):h.press(4 if delta<=16 else 5)
        if i<11:h.press(7)
    h.press(8);h.frames(30)

a.begin();check(h.read('mode')==10,'Boot introduces the adventure and playable preparation')
h.frames(80)
x=a.read('x');tick=a.read('tick');h.frames(15,[7])
check(a.read('x')==x+30 and (a.read('tick')-tick)&255==15,'Movement advances at 60 Hz')
h.press(3)
state=[a.read(n) for n in ('x','y','health','room','tick')]+[h.read('song_step'),h.read('song_tick')]
h.frames(180,[7])
check(state==[a.read(n) for n in ('x','y','health','room','tick')]+[h.read('song_step'),h.read('song_tick')],'Pause freezes world and musical position')
h.press(3);h.frames(30)
check(h.read('paused')==0 and h.read('adv_command')==10,'Resume restores the playable room')
pause_option(3)
check(a.saved('easy')==1 and a.read('health')==6,'Assistance can be enabled from pause')
pause_option(4)
check(h.read('adv_ui_page')==5,'Password can be read while paused')
check(code()==password_bytes(tasks=1,easy=1),'ROM password matches independent CRC16 encoder')
saved_code=code();h.press(0);h.frames(30)
pause_option(2)
check(h.read('adv_ui_page')==1,'Quit returns to studio with progress intact')
h.press(0);h.press(5);h.press(8);h.frames(30)
check(h.read('adv_ui_page')==8,'New game warns before erasing prepared tasks')
h.press(0);h.frames(30)
check(a.saved('tasks')==1,'Cancel new game preserves progress')
# A real console reset clears RAM; all restoration goes through the code editor.
h.core.retro_reset();h.frames(90);h.press(5);h.press(8);h.frames(30)
check(h.read('adv_ui_page')==5,'Load password is available immediately after reset')
enter_code([0]*12)
check(h.read('adv_code_error')==1 and a.saved('valid')==0,'Malformed code is rejected atomically')
h.press(0);h.frames(30);h.press(8);h.frames(30)
enter_code(password_bytes(cleared=256,tasks=7))
check(h.read('adv_code_error')==1 and a.saved('valid')==0,'Correct checksum cannot bypass campaign progression')
h.press(0);h.frames(30);h.press(8);h.frames(30)
enter_code(saved_code)
check(a.saved('tasks')==1 and a.saved('easy')==1 and h.read('adv_ui_page')==1,'Valid code restores preparation and difficulty after reset')
# Rehearse the opening room with all three actors; their movement routes agree.
for actor in range(3):
    while h.read('host')!=actor:h.press(2)
    h.press(8);h.frames(30);h.press(8);h.frames(30)
    h.frames(100)
    h.frames(1,[0]);h.frames(1)
    if actor==1:check(any(a.read('bullets',i*6+2) and a.read('bullets',i*6+3) for i in range(3)),'Estefania fires a player projectile')
    check(h.read('host')==actor,'Selected actor remains active: '+str(actor))
    a.clear_room();check(a.read('room')==1,'Opening route works for actor '+str(actor))
    pause_option(2)
# The classic collection still opens and its episode state is untouched.
h.press(0);h.frames(30)
for _ in range(3):h.press(5)
h.press(8);h.frames(30)
check(h.read('mode')==0 and h.read('completed')==0 and h.read('episode')==0,'Classic collection survives campaign rehearsal without stamps or episode changes')
h.close()
