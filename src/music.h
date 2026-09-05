/* Original six-theme NES score. One eighth-note clock drives both music and cues. */
u8 music_track,beat_flash,beat_no,music_restore;
const u8 tempos[6]={18,12,15,24,12,24};
const u8 duties[6]={0x40,0x80,0x40,0x80,0x40,0x80};
const u16 periods[37]={0,427,403,380,359,338,319,301,284,268,253,239,225,213,201,189,179,169,159,150,142,134,126,119,112,106,100,94,89,84,79,75,70,66,63,59,56};
const u8 leads[6][32]={
{13,17,20,0,17,20,22,20,17,0,15,17,20,0,17,15,13,17,20,25,24,20,17,0,18,22,20,17,15,0,13,0},
{17,0,17,20,22,20,17,15,17,12,15,17,20,17,15,12,13,17,20,22,20,17,15,13,12,15,17,20,22,20,17,0},
{13,0,20,0,22,20,17,0,18,0,22,0,20,17,15,0,13,17,20,0,25,24,22,20,18,22,20,17,15,0,20,0},
{17,0,20,0,15,0,17,0,13,0,12,0,15,0,8,0,10,0,13,0,17,0,15,0,12,0,8,0,13,0,0,0},
{13,17,20,25,0,20,22,25,24,20,17,20,25,0,0,0,18,22,25,0,17,20,25,0,15,20,24,0,25,0,0,0},
{17,0,15,0,13,0,12,0,10,0,8,0,5,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
};
const u8 basses[6][16]={
{1,1,10,10,6,6,8,8,1,1,10,10,6,8,1,8},
{5,5,5,5,1,1,3,3,5,5,1,1,10,10,12,12},
{1,1,10,10,6,6,8,8,1,1,10,10,6,6,8,8},
{1,1,5,5,10,10,8,8,6,6,5,5,3,8,1,1},
{1,1,6,6,8,8,1,1,6,6,1,1,8,8,1,1},
{10,10,8,8,6,6,5,5,5,5,5,5,5,5,5,5}
};

void silence(void){REG(0x4000)=0x10;REG(0x4004)=0x10;REG(0x4008)=0;REG(0x400c)=0x10;}
void music_start(u8 track){
 silence();music_track=track;song_tick=0;song_step=0;beat_no=0;beat_flash=0;sfx_tick=0;music_restore=0;
}
void sound(u8 effect){
 /* Pulse 2 is reserved for short feedback; the beat and melody keep playing. */
 sfx_tick=6;REG(0x4004)=effect==2?0x94:0x52;REG(0x4005)=0;
 REG(0x4006)=effect==1?100:(effect==2?220:70);REG(0x4007)=effect==2?0xfa:0xf8;
}
void music_note(void){u8 note;u16 period;
 note=leads[music_track][song_step];
 if(note){period=periods[note];REG(0x4000)=duties[music_track]|0x14;
  REG(0x4002)=(u8)period;REG(0x4003)=0xf8|(u8)(period>>8);
 }else REG(0x4000)=0x10;
 if(!(song_step&1)){
  beat_no=(song_step>>1)&3;if(!song_tick)beat_flash=6;
  period=periods[basses[music_track][song_step>>1]];
  REG(0x4008)=0x88;REG(0x400a)=(u8)period;REG(0x400b)=0xf8|(u8)(period>>8);
 }
 if(song_tick){if(song_tick>=8)REG(0x4008)=0;return;}
 /* Estefi's quarter-note kick/snare is louder than the offbeat hi-hat. */
 if(music_track==2){
  REG(0x400c)=(song_step&1)?0x12:0x17;
  REG(0x400e)=(song_step&1)?3:((song_step&2)?10:13);
 }else if(music_track==3){REG(0x400c)=0x11;REG(0x400e)=4;}
 else{REG(0x400c)=(song_step&1)?0x11:0x14;REG(0x400e)=(song_step&2)?9:3;}
 REG(0x400f)=0xf8;
}
void audio(void){
 if(sfx_tick){--sfx_tick;if(!sfx_tick)REG(0x4004)=0x10;}
 if(beat_flash)--beat_flash;
 if(!song_tick||music_restore){music_note();music_restore=0;}
 if(song_tick==3)REG(0x400c)=0x10;
 if(song_tick==8){REG(0x4000)=leads[music_track][song_step]?(duties[music_track]|0x11):0x10;REG(0x4008)=0;}
 if(++song_tick==tempos[music_track]){song_tick=0;song_step=(song_step+1)&31;}
}
