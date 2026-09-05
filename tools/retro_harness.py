"""Independent hardware smoke test via the FCEUmm libretro core."""
import ctypes as C
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
core=C.CDLL(str(root/'tools/fceumm/fceumm_libretro.dll'))
Env=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
Video=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
Audio=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
Batch=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
Poll=C.CFUNCTYPE(None)
Input=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
class Game(C.Structure):
    _fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
pixel_format=0
screen=None
buttons=set()
audio_peak=0
capture_audio=False
audio_samples=bytearray()
@Env
def env(cmd,data):
    global pixel_format
    if cmd==10:
        pixel_format=C.cast(data,C.POINTER(C.c_int))[0];return True
    if cmd==3:return True # frame duplication supported
    if cmd==15: # core option: return default
        C.cast(data,C.POINTER(C.c_void_p))[1]=None;return False
    if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
    if cmd==18:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
    return False
@Video
def video(data,w,h,pitch):
    global screen
    if data:screen=(C.string_at(data,pitch*h),w,h,pitch,pixel_format)
@Audio
def audio(l,r):
    global audio_peak
    audio_peak=max(audio_peak,abs(l),abs(r))
    if capture_audio:audio_samples.extend(int(l).to_bytes(2,"little",signed=True)+int(r).to_bytes(2,"little",signed=True))
@Batch
def batch(data,n):
    global audio_peak
    if n:audio_peak=max(audio_peak,max(abs(data[i]) for i in range(0,n*2,16)))
    if capture_audio:audio_samples.extend(C.string_at(data,n*4))
    return n
@Poll
def poll():pass
@Input
def inp(port,device,index,key):return int(port==0 and key in buttons)
for name,cb in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',inp)]:
    fn=getattr(core,'retro_set_'+name);fn.argtypes=[type(cb)];fn(cb)
core.retro_init()
core.retro_load_game.argtypes=[C.POINTER(Game)];core.retro_load_game.restype=C.c_bool
core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
core.retro_get_memory_size.argtypes=[C.c_uint];core.retro_get_memory_size.restype=C.c_size_t
rom=(root/'build/el-cuartico.nes').read_bytes();buf=C.create_string_buffer(rom)
g=Game(str(root/'build/el-cuartico.nes').encode(),C.cast(buf,C.c_void_p),len(rom),None)
assert core.retro_load_game(C.byref(g))
core.retro_set_controller_port_device(0,1)
ram=core.retro_get_memory_data(2)
assert ram and core.retro_get_memory_size(2)>=2048
labels={}
for line in (root/'build/el-cuartico.lbl').read_text().splitlines():
    _,addr,name=line.split();labels[name.lstrip('.')]=int(addr,16)
def read(name):return C.c_uint8.from_address(ram+labels['_'+name]).value
def frames(n,keys=()):
    global buttons
    buttons=set(keys)
    for _ in range(n):core.retro_run()
def press(key):frames(5,[key]);frames(15)

def screenshot(name):
    raw,w,h,pitch,fmt=screen
    im=Image.new('RGB',(w,h))
    for y in range(h):
        for x in range(w):
            size=4 if fmt==1 else 2
            value=int.from_bytes(raw[y*pitch+x*size:y*pitch+(x+1)*size],'little')
            if fmt==1:rgb=((value>>16)&255,(value>>8)&255,value&255)
            elif fmt==2:rgb=(((value>>11)&31)*255//31,((value>>5)&63)*255//63,(value&31)*255//31)
            else:rgb=(((value>>10)&31)*255//31,((value>>5)&31)*255//31,(value&31)*255//31)
            im.putpixel((x,y),rgb)
    im.save(root/'build'/name)

def close():
    core.retro_unload_game();core.retro_deinit()
