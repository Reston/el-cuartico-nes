"""Real-controller checks for the v0.5 plaza and music/beat contract."""
import hashlib, wave, struct, math
import retro_harness as h
from play_helpers import target_area
report=[]
def read(n,i=0):return h.C.c_uint8.from_address(h.ram+h.labels['_'+n]+i).value
def check(ok,msg):
    line=('PASS ' if ok else 'FAIL ')+msg;report.append(line);print(line,flush=True)
    (h.root/'build/plaza-music-tests.txt').write_text('\n'.join(report)+'\n')
    assert ok,msg
def boot(host=None):
    h.core.retro_reset();h.frames(90)
    if host is not None:
        for _ in range(host):h.press(7)
        h.press(3)
def pulse(key):h.frames(1,[key]);h.frames(1)
def state():return tuple(read(n) for n in ['song_tick','song_step','rhythm_phase','count_in','hits','misses'])+tuple(read('note_age',i) for i in range(3))
def capture(name,n=360):
    h.audio_samples.clear();h.capture_audio=True;h.frames(n);h.capture_audio=False
    pcm=bytes(h.audio_samples)
    # FCEUmm's libretro audio sample rate is reported by the core, not assumed.
    class Geometry(h.C.Structure):_fields_=[('bw',h.C.c_uint),('bh',h.C.c_uint),('mw',h.C.c_uint),('mh',h.C.c_uint),('aspect',h.C.c_float)]
    class Timing(h.C.Structure):_fields_=[('fps',h.C.c_double),('sample_rate',h.C.c_double)]
    class AV(h.C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
    av=AV();h.core.retro_get_system_av_info(h.C.byref(av))
    with wave.open(str(h.root/'build'/name),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(round(av.timing.sample_rate));w.writeframes(pcm)
    vals=struct.unpack('<'+str(len(pcm)//2)+'h',pcm)
    check(len(pcm)>100000 and max(abs(v) for v in vals)>100,'Audible PCM captured: '+name)
    check(max(abs(v) for v in vals)<32767,'No full-scale PCM clipping: '+name)
    return hashlib.sha256(pcm).hexdigest()
rom=(h.root/'build/el-cuartico.nes').read_bytes()
check(len(rom)==393232 and rom[:8]==b'NES\x1a\x08\x20\x50\x00','MMC5 header and PRG/CHR ROM sizes agree')
# Each mode selects a distinct composition/tempo, with actual PCM output.
fingerprints=[]
for host,track,name in [(None,0,'music-intro.wav'),(0,1,'music-chucho.wav'),(1,2,'music-estefania.wav'),(2,3,'music-daniel.wav')]:
    boot(host);check(read('music_track')==track,'Correct music for '+name)
    fingerprints.append(capture(name))
check(len(set(fingerprints))==4,'All four recorded themes differ')
# Each three-beat flight reaches its marker on a music beat, including after pause.
boot(1);pulse(8)
check(read('cue_demo')==0 and read('count_in')>100,'Practice A starts a four-beat count-in')
h.frames(40);h.screenshot('rhythm-count-in.png')
while read('count_in'):h.frames(1)
centers=[];pauses=0;shot=False
for f in range(3000):
    if read('mode')!=2:break
    if pauses<3 and f>=[120,420,900][pauses] and read('cue_head')<3 and 20<=read('note_age',read('cue_head'))<=40:
        pulse(3);before=state();h.frames(97);check(state()==before,'Pause freezes beat and cue clocks together')
        pulse(3);pauses+=1
    head=read('cue_head');keys=[]
    if head<3 and read('note_age',head)==90:
        centers.append((read('song_tick'),read('song_step')%2))
        keys=[[8,0,6,7,4,5][read('note_key',head)]]
    if not shot and sum(read('note_live',i) for i in range(3))==2 and read('cue_x')<110:
        h.screenshot('rhythm-on-beat.png');shot=True
    h.frames(1,keys)
check(read('hits')==20 and read('last_win')==1,'Beat-center controller presses complete Estefania with no drift')
check(read('misses')==0 and len(centers)==19 and len(set(centers))==1,'All 19 chart cues align with the same beat phase without misses')
check(centers[0]==(1,0),'Cue center coincides with the quarter-note attack frame')
check(pauses==3,'Beat synchronization survives three pauses')
# Early, wrong, late and held buttons must not be rewarded as beat hits.
for case in ['early','wrong','late','held']:
    boot(1);pulse(8)
    while read('count_in'):h.frames(1)
    while read('cue_head')==255:h.frames(1)
    if case=='early':pulse(8)
    elif case=='wrong':
        while read('note_age',read('cue_head'))<90:h.frames(1)
        pulse(0) # First chart note is A.
    elif case=='late':h.frames(105)
    else:h.frames(110,[8])
    check(read('hits')==1 and read('misses')>=1,'No free rhythm credit for '+case+' input')
# Free cursor movement, unique target, readable full-body slots and fresh hiding spot.
boot(2)
for scene in range(3):
    h.frames(40);check(read('bg_bank')==1,'Plaza background active in search '+str(scene+1))
    target_area()
    n=read('crowd_count');coords=[(read('npc_x',i),read('npc_y',i)) for i in range(n)]
    check(n==12+scene*4 and len(set(coords))==n,'Scattered distinct hiding positions for scene '+str(scene+1))
    check(sum(read('crowd',i)==0 for i in range(n))==1,'Exactly one true Daniel in scene '+str(scene+1))
    h.screenshot('plaza-scene-'+str(scene+1)+'.png')
    for _ in range(400):
        t=read('target');x=read('npc_x',t);y=read('npc_y',t)+4
        if read('cursor_x')<x:key=7
        elif read('cursor_x')>x:key=6
        elif read('cursor_y')<y:key=5
        elif read('cursor_y')>y:key=4
        else:break
        h.frames(1,[key])
    h.frames(1);pulse(8)
    if scene<2:
        while read('round_no')==scene:h.frames(1)
    else:h.frames(40)
check(read('completed')==4 and read('last_win')==1,'Free cursor clears all plaza searches')
h.press(3);check(read('mode')==0 and read('bg_bank')==0,'Leaving plaza restores studio graphics')
h.screenshot('plaza-return-hub.png')
h.close();report.append('ALL PLAZA AND MUSIC CHECKS PASSED')
(h.root/'build/plaza-music-tests.txt').write_text('\n'.join(report)+'\n')
