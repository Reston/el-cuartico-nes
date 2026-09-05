/* El Cuartico v0.8: three games, freely ordered, one shared episode. */
typedef unsigned char u8;
typedef unsigned int u16;
#define REG(a) (*(volatile u8*)(a))
#define PPUCTRL REG(0x2000)
#define PPUMASK REG(0x2001)
#define PPUADDR REG(0x2006)
#define PPUDATA REG(0x2007)
#define OAM ((u8*)0x0200)
#define A 128
#define B 64
#define SELECT 32
#define START 16
#define UP 8
#define DOWN 4
#define LEFT 2
#define RIGHT 1
#define HUB 0
#define REPAIR 1
#define RHYTHM 2
#define SEARCH 3
#define RESULT 4
#define ENDING 5
#define SPR_BASE 0
#define SPARK 236
#define CROSS 237
#define HEART 238
#define EMPTY_HEART 239
#define DIGITS 242
#define MEDAL 255
extern void wait_frame(void);
extern u8 pad_read(void);
extern void __fastcall__ chr_bank(u8 bank);
extern volatile u8 frame,ready,hud_on,art_bank,sprite_bank;
extern u8 hud[32],menu_rows[96];
extern volatile u8 menu_dirty;
extern volatile u8 ex_on;
extern void title_extended(void);
extern const u8 studio[1024],title[1024],stage[1024],plaza[3072],districts[4096];

/* Exposed symbols support real-controller emulator integration tests. */
u8 mode,host,completed,last_win,seconds,health,carry,combo,paused;
u8 px,py,pad,oldpad,pressed,tick,spawn_in,rng,anim_tick,facing;
u8 alarm[4],cooldown,dashing,feedback,flash,spr,walk,hud_dirty;
u8 song_tick,song_step,sfx_tick,repairs,misses,first_repair;
u8 cue_x,cue_key,cue_wait,cue_demo,hits,pose;
u8 judgement,perfects,zoom_npc;
u8 rhythm_chain,peak_chain,cheer,hover_npc,feedback_x,feedback_y,result_grade;
u8 note_age[3],note_key[3],note_live[3],cue_head,chart_step,count_in,rhythm_phase;
u8 round_no,found,cursor_col,cursor_row,cols,rows,origin_x,origin_y;
u8 crowd[24],target,search_wait,dir_repeat,previous_target;
u8 npc_x[24],npc_y[24],crowd_count,cursor_x,cursor_y,spots[24],plaza_attrs[64],bg_bank;
u8 district,district_count,target_district,world_seed,scene_bank,visited,travel_lock;
u8 studio_charge,studio_station,studio_stun,studio_guard,cable_x;
u8 task_active,repair_task,task_progress,task_cursor,task_value,task_target,task_phase,task_error;
u16 task_frame;
u8 task_order[3],task_code[4];
u16 score,best,attempt_score;
const u8 sx[4]={40,216,40,216};
const u8 sy[4]={80,80,152,152};
const u8 masks[3]={1,2,4};
const u8 cue_masks[6]={A,B,LEFT,RIGHT,UP,DOWN};
/* Exact Daniel is type 0. Each other face changes hair, glasses or facial hair. */
const u8 faces[24]={24,25,26,27, 0,1,2,3, 12,13,14,15,
                   24,25,2,3, 0,1,26,27, 12,13,2,3};
const char* const names[3]={"CHUCHO","ESTEFANIA","DANIEL"};
const char* const titles[3]={"LA GRABACION","EL SKETCH","DONDE ESTA DANIEL?"};
const char* const goals[3]={"12 TOMAS EN VIVO","20 ACIERTOS","3 ENCUENTROS"};
const u8 palette[32]={
 0x0f,0x07,0x27,0x30, 0x0f,0x07,0x17,0x27,
 0x0f,0x07,0x17,0x37, 0x0f,0x00,0x10,0x30,
 0x0f,0x0f,0x37,0x27, 0x0f,0x0f,0x37,0x21,
 0x0f,0x0f,0x37,0x16, 0x0f,0x16,0x27,0x30
};
const u8 title_palette[16]={
 0x0f,0x07,0x27,0x30, 0x0f,0x0f,0x27,0x37,
 0x0f,0x0f,0x11,0x21, 0x0f,0x0f,0x37,0x16
};
const u8 stage_palette[16]={
 0x0f,0x07,0x27,0x30, 0x0f,0x06,0x16,0x26,
 0x0f,0x07,0x17,0x37, 0x0f,0x04,0x14,0x34
};
const u8 plaza_palette[3][16]={
 {0x37,0x07,0x27,0x30, 0x37,0x0f,0x27,0x16, 0x37,0x0b,0x1a,0x29, 0x37,0x01,0x21,0x31},
 {0x30,0x01,0x21,0x31, 0x30,0x0f,0x37,0x16, 0x30,0x0b,0x1a,0x29, 0x30,0x01,0x21,0x31},
 {0x37,0x07,0x25,0x30, 0x37,0x0f,0x27,0x16, 0x37,0x0b,0x19,0x25, 0x37,0x01,0x21,0x31}
};
/* Hiding places follow the paths around props, rather than a selectable grid. */
const u8 place_x[24]={16,48,80,112,160,192,224,64,176,32,96,128,208,16,64,160,208,112,144,80,160,48,224,192};
const u8 place_y[24]={96,96,96,96,96,96,96,112,112,144,176,176,144,160,176,176,176,192,112,128,144,160,176,192};
const u8 hero_dx[15]={0,8,16,0,8,16,0,8,16,0,8,16,0,8,16};
const u8 hero_dy[15]={0,0,0,8,8,8,16,16,16,24,24,24,32,32,32};
const u8 hero_base[4]={96,111,126,141};
const u8 cue_chart[32]={0,0,1,1,2,3,0,1,4,5,0,1,2,2,3,3,0,4,1,5,2,0,3,1,4,0,5,1,2,3,0,1};

void start_game(void);
void task_step(void);
void task_draw(void);
void task_open(u8 station);
void hub(void);
void finish(u8 won);
void hud_update(void);
void search_scene(void);
u8 cursor_person(void);
void addr(u16 a){PPUADDR=(u8)(a>>8);PPUADDR=(u8)a;}
void print(u8 x,u8 y,const char* s){addr(0x2000+((u16)y<<5)+x);while(*s)PPUDATA=*s++;}
void center(u8 y,const char* s){u8 n=0;while(s[n])++n;print((32-n)/2,y,s);}
void line_clear(u8 y){u8 i;addr(0x2000+((u16)y<<5));for(i=0;i<32;++i)PPUDATA=32;}
void number(u8 x,u8 y,u16 n){u8 b[5],i;for(i=0;i<5;++i){b[4-i]='0'+n%10;n/=10;}addr(0x2000+((u16)y<<5)+x);for(i=0;i<5;++i)PPUDATA=b[i];}
extern void hide(void);
extern void sprite(u8 x,u8 y,u8 tile,u8 pal);
void person(u8 x,u8 y,u8 who,u8 step){u8 i,base=step<2?who*12+step*6:56+who*12+(step-2)*6;for(i=0;i<6;++i)sprite(x+(i&1)*8,y+(i>>1)*8,base+i,who);}
void token(u8 x,u8 key){u8 i;for(i=0;i<4;++i)sprite(x-4+(i&1)*8,172+(i>>1)*8,156+key*4+i,3);}
void focus(u8 x,u8 y,u8 pal){sprite(x,y,48,pal);sprite(x+12,y,49,pal);sprite(x,y+12,50,pal);sprite(x+12,y+12,51,pal);}
void off(void){PPUCTRL=0;PPUMASK=0;ex_on=0;REG(0x5104)=2;ready=0;hud_on=0;menu_dirty=0;hide();}
void on(void){REG(0x2005)=0;REG(0x2005)=0;PPUCTRL=0x88;PPUMASK=0x1e;}
void background(const u8* data){u16 i;addr(0x2000);for(i=0;i<1024;++i)PPUDATA=data[i];}
void load_palette(const u8* data,u8 count){u8 i;addr(0x3f00);for(i=0;i<count;++i)PPUDATA=data[i];}
void blank(void){u16 i;off();chr_bank(0);bg_bank=0;load_palette(palette,32);addr(0x2000);for(i=0;i<960;++i)PPUDATA=32;for(i=0;i<64;++i)PPUDATA=0;}
#include "music.h"
u8 random(void){rng^=rng<<3;rng^=rng>>5;rng^=rng<<1;if(!rng)rng=91;return rng;}
u8 is_near(u8 x,u8 y){int dx=(int)px+8-x,dy=(int)py+16-y;return dx>-23&&dx<23&&dy>-23&&dy<23;}
void hud_text(const char* s){u8 i=0;while(*s&&i<32)hud[i++]=*s++;while(i<32)hud[i++]=32;}
void hud_two(u8 p,u8 n){hud[p]='0'+n/10;hud[p+1]='0'+n%10;}
void hud_update(void){
 if(paused){hud_text(" START:SIGUE A:RETRY B:SALIR");return;}
 if(mode==REPAIR){hud_text(" EN VIVO 00/12 75S RACHA X1");hud_two(9,repairs);hud_two(15,seconds);hud[26]='0'+combo;}
 else if(mode==RHYTHM){hud_text(" SKETCH 00/20 X00 FALLOS 0/5");hud_two(8,hits);hud_two(15,rhythm_chain);hud[25]='0'+misses;}
 else if(mode==SEARCH){hud_text(" BUSCA 0/3     60S      A:ELIGE");hud[7]='0'+found;hud_two(15,seconds);hud[19]='Z';hud[20]='O';hud[21]='N';hud[22]='A';hud[23]=' ' ;hud[24]='1'+district;hud[25]='/';hud[26]='0'+district_count;hud[27]=hud[28]=hud[29]=hud[30]=hud[31]=32;}
 hud_dirty=0;
}
/* Publish the three labels together; NMI commits them with the new OAM. */
void menu_selection(void){
 u8 i,j,n;const char* s;
 for(i=0;i<96;++i)menu_rows[i]=32;
 for(j=0;j<3;++j){
  s=j==0?titles[host]:(j==1?names[host]:((completed&masks[host])?"LISTO!":goals[host]));
  n=0;while(s[n])++n;
  i=j*32+(32-n)/2;while(*s)menu_rows[i++]=*s++;
 }
 menu_dirty=1;
}

void hub(void){
 u8 i;off();chr_bank(0);bg_bank=0;anim_tick=0;if(music_track!=0)music_start(0);paused=0;load_palette(palette,32);load_palette(title_palette,16);background(title);title_extended();
 line_clear(14);center(14,titles[host]);line_clear(24);center(24,names[host]);
 line_clear(26);center(26,(completed&masks[host])?"LISTO!":goals[host]);
 for(i=0;i<3;++i)if(completed&masks[i])print(6+i*8,23,"OK");
 mode=HUB;on();
}
void ending(void){
 off();chr_bank(0);bg_bank=0;music_start(4);paused=0;if(score>best)best=score;load_palette(palette,32);load_palette(title_palette,16);background(title);title_extended();
 line_clear(14);center(14,"EPISODIO PUBLICADO!");line_clear(24);print(7,24,"PUNTOS");number(17,24,score);
 line_clear(26);center(26,"LOS TRES LO HICIERON");line_clear(28);center(28,"START: NUEVO EPISODIO");mode=ENDING;on();
}
void finish(u8 won){
 last_win=won;paused=0;result_grade=won?(misses==0?3:(misses<=2?2:1)):0;
 if(won){if(!(completed&masks[host]))score+=attempt_score;completed|=masks[host];sound(1);if(completed==7){ending();return;}}
 else sound(2);
 blank();load_palette(title_palette,16);background(title);title_extended();
 line_clear(14);center(14,won?(result_grade==3?"TOMA PERFECTA!":"LISTO!"):"OTRA TOMA");line_clear(24);center(24,names[host]);
 line_clear(26);print(7,26,"PUNTOS");number(17,26,attempt_score);
 line_clear(28);center(28,won?"START: SIGUE":"A: RETRY  B: SALIR");
 mode=RESULT;music_start(won?4:5);on();
}
void search_person(u8 x,u8 y,u8 type){u8 row,i,t,body;
 body=type==0?28:(type==2||type==5?16:4);
 for(row=0;row<3;++row){addr(0x2000+((u16)(y/8+row)<<5)+x/8);
  for(i=0;i<2;++i){t=row==2?body+i:faces[type*4+row*2+i];PPUDATA=220+t;}}
}
void search_scene(void){u8 i,j,k,swap,x,y,at,shift,saved_rng;const u8* area;
 off();mode=SEARCH;scene_bank=12+round_no*4;
 area=plaza+((u16)round_no<<10);
 if(district){i=round_no==1?0:district;scene_bank=30+i*4;area=districts+((u16)i<<10);}
 chr_bank(scene_bank);bg_bank=1;visited|=1<<district;
 saved_rng=rng;rng=world_seed+district*37;if(!rng)rng=91;
load_palette(palette,32);load_palette(plaza_palette[round_no],16);
 /* A dark cursor stays visible over the light stone paving. */
 addr(0x3f1f);PPUDATA=0x0f;background(area);
 /* Original full-body people sit on the plaza paths; the exact face occurs once. */
 crowd_count=12+round_no*4;
 for(i=0;i<24;++i)spots[i]=i;
 for(i=23;i>0;--i){j=random()%(i+1);swap=spots[i];spots[i]=spots[j];spots[j]=swap;}
 target=random()%crowd_count;
 if(!round_no){
  if(spots[target]==previous_target){j=(target+1)%crowd_count;swap=spots[target];spots[target]=spots[j];spots[j]=swap;}
  previous_target=spots[target];
 }
 if(district!=target_district)target=255;
 for(i=0;i<64;++i)plaza_attrs[i]=area[960+i];
 for(i=0;i<crowd_count;++i){
  npc_x[i]=place_x[spots[i]];npc_y[i]=place_y[spots[i]];
  crowd[i]=i==target?0:1+random()%5;search_person(npc_x[i],npc_y[i],crowd[i]);
  x=npc_x[i]/16;y=npc_y[i]/16;
  for(k=0;k<2;++k){at=((y+k)/2)*8+x/2;shift=(((y+k)&1)*2+(x&1))*2;
   plaza_attrs[at]=(plaza_attrs[at]&~(3<<shift))|(1<<shift);}
 }
 addr(0x23c0);for(i=0;i<64;++i)PPUDATA=plaza_attrs[i];
 print(5,4,"BUSCA");print(18,4,"DANIEL");
 /* Navigation occupies only row 28, below every person and cursor rectangle. */
 line_clear(28);
 if(district_count==1)center(28,"A:BUSCA B:LUPA");
 else{
  print(1,28,"CRUZA:");
  if(district&1)print(9,28,"<");
  if(!(district&1)&&district_count>1)print(12,28,">");
  if(district>=2)print(15,28,"SUBE");
  if(district_count==4&&district<2)print(21,28,"BAJA");
 }
 rng=saved_rng;hover_npc=cursor_person();feedback=0;search_wait=0;travel_lock=12;
 hud_update();hud_on=1;on();
}
void search_round(void){
 district=0;district_count=1<<round_no;visited=0;world_seed=random();
 target_district=random()%district_count;
 seconds=round_no==0?60:(round_no==1?85:99);tick=0;cursor_x=120;cursor_y=176;
 search_scene();
}
void travel(u8 next,u8 x,u8 y){district=next;cursor_x=x;cursor_y=y;search_scene();}
void start_game(void){
 u8 i;task_active=0;off();chr_bank(0);bg_bank=0;music_start(host+1);paused=0;attempt_score=0;health=5;misses=0;tick=0;feedback=0;carry=0;hud_dirty=0;cheer=0;rhythm_chain=0;peak_chain=0;hover_npc=255;
 if(host==0){off();chr_bank(4);facing=0;anim_tick=0;load_palette(palette,32);background(studio);mode=REPAIR;
  seconds=75;repairs=0;combo=1;first_repair=1;spawn_in=4;studio_charge=0;studio_station=255;studio_stun=0;studio_guard=0;cable_x=24;px=120;py=144;cooldown=0;dashing=0;walk=0;
  for(i=0;i<4;++i)alarm[i]=0;alarm[0]=14;alarm[1]=18;hud_update();hud_on=1;on();
 }else if(host==1){off();chr_bank(8);anim_tick=0;load_palette(palette,32);load_palette(stage_palette,16);addr(0x3f13);PPUDATA=0x30;background(stage);mode=RHYTHM;
  hits=0;perfects=0;judgement=0;cue_key=0;cue_x=60;cue_demo=1;cue_wait=0;pose=0;count_in=0;rhythm_phase=0;chart_step=0;cue_head=255;
  for(i=0;i<3;++i)note_live[i]=0;hud_update();hud_on=1;on();
 }else{round_no=0;found=0;search_round();}
}
void move(void){u8 nx=px,ny=py,speed=2;
 if(cooldown)--cooldown;
 if((pressed&B)&&!cooldown){dashing=10;cooldown=50;sound(3);}
 if(dashing){--dashing;speed=4;}
 if(pad&LEFT){facing=1;if(nx>=16+speed)nx-=speed;else nx=16;}
 if(pad&RIGHT){facing=0;if(nx<=224-speed)nx+=speed;else nx=224;}
 if(pad&UP){if(ny>=56+speed)ny-=speed;else ny=56;}
 if(pad&DOWN){if(ny<=176-speed)ny+=speed;else ny=176;}
 if(!(nx+13>80&&nx+3<176&&py+23>88&&py+17<136))px=nx;
 if(!(px+13>80&&px+3<176&&ny+23>88&&ny+17<136))py=ny;
 if(pad&15)++walk;
}
void studio_success(u8 i){
 alarm[i]=0;studio_charge=0;attempt_score+=100*combo;if(combo<5)++combo;
 ++repairs;feedback=35;flash=i;hud_dirty=1;sound(1);
 if(!(repairs&3)){seconds=seconds<97?seconds+3:99;cheer=30;}
 if(repairs==12){attempt_score+=seconds*10;finish(1);}
}
u8 studio_near(u8 i){return i==1?(px>=184&&py<=104):is_near(sx[i],sy[i]);}
void repair_action(void){u8 i;studio_station=255;
 for(i=0;i<4;++i)if(alarm[i]&&studio_near(i)){studio_station=i;break;}
 if((pressed&A)&&studio_station<4)task_open(studio_station);
}
void studio_step(void){
 if(task_active){task_step();return;}
 move();repair_action();
}
void task_close(void){
 task_active=0;off();chr_bank(4);load_palette(palette,32);background(studio);
 hud_update();hud_on=1;on();
}
void task_win(void){task_active=0;studio_success(repair_task);if(mode==REPAIR)task_close();}
void task_open(u8 station){u8 i,x,y;
 repair_task=station;task_active=1;task_progress=0;task_cursor=0;task_value=0;
 task_target=station==2?12+random()%40:16+random()%28;task_phase=0;task_frame=0;task_error=0;
 x=random()%3;for(i=0;i<3;++i)task_order[i]=(i+x)%3;
 for(i=0;i<4;++i)task_code[i]=random()&3;
 off();chr_bank(4);load_palette(palette,32);background(studio);
 /* A framed console with short labels; interactive pieces are OAM sprites. */
 for(y=4;y<28;++y){addr(0x2000+((u16)y<<5)+2);for(x=2;x<30;++x)PPUDATA=32;}
 center(5,"--------------------------");center(23,"--------------------------");
 center(25,"B: VOLVER");line_clear(28);center(28,"REPARACION EN CURSO");
 if(station==0){center(7,"CABLES");center(21,"UNE NUMEROS  A:CONECTA");
  for(i=0;i<3;++i){addr(0x2000+((u16)(11+i*4)<<5)+8);PPUDATA='1'+i;
   addr(0x2000+((u16)(11+i*4)<<5)+23);PPUDATA='1'+task_order[i];}
 }else if(station==1){center(7,"ENFOQUE");center(11,"<     CAMARA     >");center(19,"ALINEA  A:CONFIRMA");}
 else if(station==2){center(7,"MEZCLADORA");center(11,"ATRAPA LA SENAL");center(19,"A: EN EL RECUADRO");}
 else{center(7,"REINICIA LA SENAL");center(19,"MIRA Y REPITE");}
 hud_update();hud_on=1;on();
}
void task_step(void){u8 key=255,i;
 if(pressed&B){task_close();return;}
 if(task_error)--task_error;
 if(repair_task==0){
  if(pressed&UP)task_cursor=task_cursor?task_cursor-1:2;
  if(pressed&DOWN)task_cursor=(task_cursor+1)%3;
  if(pressed&A){if(task_order[task_cursor]==task_progress){++task_progress;sound(1);if(task_progress==3){task_win();return;}}
   else{task_error=18;sound(2);}}
 }else if(repair_task==1){
  if((pad&LEFT)&&task_value) --task_value;
  if((pad&RIGHT)&&task_value<60)++task_value;
  if(pressed&A){if(task_value+2>=task_target&&task_value<=task_target+2){
    ++task_progress;sound(1);if(task_progress==2){task_win();return;}task_target=task_target<30?46:18;
   }else{task_error=18;sound(2);}}
 }else if(repair_task==2){
  task_phase=(task_phase+1)&127;task_value=task_phase<64?task_phase:127-task_phase;
  if(pressed&A){if(task_value+5>=task_target&&task_value<=task_target+5){++task_progress;sound(1);task_phase=0;task_value=0;
    if(task_progress==3){task_win();return;}
    task_target=12+(task_target-12+8+random()%25)%40;}
   else{task_error=18;sound(2);}}
 }else{
  if(!task_phase){if(++task_frame==320){task_phase=1;task_frame=0;}return;}
  for(i=0;i<4;++i)if(pressed&cue_masks[2+i])key=i;
  if(key<4){if(key==task_code[task_progress]){++task_progress;sound(1);if(task_progress==4){task_win();return;}}
   else{task_error=18;task_progress=0;task_frame=0;task_phase=0;sound(2);}}
 }
}
void task_draw(void){u8 i,x,y;
 if(repair_task==0){
  for(i=0;i<3;++i){y=88+i*32;
   sprite(80,y,i<task_progress?39:40,3);
   sprite(168,y,task_order[i]<task_progress?39:40,3);
  }
  sprite(52,88+task_progress*32,45,3);sprite(200,88+task_cursor*32,44,3);
 }else if(repair_task==1||repair_task==2){
  x=task_target;
  sprite(56+x*2,112,48,3);sprite(72+x*2,112,49,3);
  sprite(56+x*2,132,50,3);sprite(72+x*2,132,51,3);
  sprite(64+task_value*2,123,SPARK,3);
  for(i=0;i<(repair_task==1?2:3);++i)sprite(104+i*16,168,i<task_progress?39:40,3);
 }else{
  if(!task_phase){x=task_frame/80;
   if((task_frame%80)<60)for(i=0;i<4;++i)sprite(120+(i&1)*8,104+(i>>1)*8,156+(task_code[x]+2)*4+i,3);
   sprite(124,144,40,3);
  }else{for(i=0;i<4;++i)sprite(100+i*16,112,44+i,3);sprite(124,144,42,3);}
  for(i=0;i<4;++i)sprite(100+i*16,168,i<task_progress?39:40,3);
 }
 if(task_error)sprite(124,64,CROSS,3);
}
void repair_second(void){u8 i,j;hud_dirty=1;
 for(i=0;i<4;++i)if(alarm[i]){--alarm[i];if(!alarm[i]){if(health)--health;++misses;combo=1;sound(2);}}
 if(!health){finish(0);return;}
 if(!--seconds){finish(0);return;}
 if(!--spawn_in){first_repair=(first_repair+1)&3;j=first_repair;
  for(i=0;i<4;++i){if(!alarm[j]){alarm[j]=repairs<4?14:11;break;}j=(j+1)&3;}
  spawn_in=repairs<4?4:3;
 }
}
void cue_result(u8 success){
 feedback=16;hud_dirty=1;
 judgement=0;if(success&&cue_head<3&&note_age[cue_head]>=87&&note_age[cue_head]<=93){judgement=1;++perfects;attempt_score+=50;}
 if(success&&cue_head<3){
  ++rhythm_chain;if(rhythm_chain>peak_chain)peak_chain=rhythm_chain;
  if(rhythm_chain%5==0){attempt_score+=100;cheer=24;}
 }else if(!success){rhythm_chain=0;cheer=0;}
 if(cue_head<3)note_live[cue_head]=0;
 if(success){++hits;attempt_score+=100;pose=cue_key;sound(1);if(hits==20){finish(1);return;}}
 else{++misses;pose=6;sound(2);if(misses==5){finish(0);return;}}
}
void cue_front(void){u8 i;cue_head=255;cue_wait=1;
 for(i=0;i<3;++i)if(note_live[i]&&(cue_head==255||note_age[i]>note_age[cue_head]))cue_head=i;
 if(cue_head<3){cue_wait=0;cue_key=note_key[cue_head];cue_x=240-note_age[cue_head]*2;}
}
void rhythm_step(void){u8 keys,i;
 keys=pressed&(A|B|UP|DOWN|LEFT|RIGHT);
 if(cue_demo){if(keys==A){cue_demo=0;cue_head=255;cue_result(1);count_in=120;rhythm_phase=0;music_start(2);cue_wait=1;}return;}
 if(count_in){--count_in;return;}
 /* Cue age 90 is the target center, exactly three 30-frame beats after spawn.
    A new cue enters every two beats; input never changes the music clock. */
 for(i=0;i<3;++i)if(note_live[i])++note_age[i];
 if(!rhythm_phase){for(i=0;i<3;++i)if(!note_live[i]){
  note_live[i]=1;note_age[i]=0;note_key[i]=cue_chart[chart_step];chart_step=(chart_step+1)&31;break;}}
 if(++rhythm_phase==60)rhythm_phase=0;
 cue_front();
 if(cue_head<3){
  if(keys)cue_result(keys==cue_masks[cue_key]&&note_age[cue_head]>=82&&note_age[cue_head]<=98);
  else if(note_age[cue_head]>98)cue_result(0);
 }
 cue_front();
}
/* One nearest-person rule drives both the lens and A. Overlapping hit boxes
   can no longer show a decoy in the lens while submitting Daniel underneath. */
u8 cursor_person(void){u8 i,best_npc=255,distance,best_distance=255,dx,dy,x,y;
 for(i=0;i<crowd_count;++i){
  x=npc_x[i];dx=cursor_x>x?cursor_x-x:x-cursor_x;
  if(dx>10)continue;
  y=npc_y[i]+4;dy=cursor_y>y?cursor_y-y:y-cursor_y;
  if(dy>14)continue;
  distance=dx+dy;
  if(distance<best_distance){best_distance=distance;best_npc=i;}
 }
 return best_npc;
}
void search_step(void){u8 speed=pad&B?1:2,moved=0;
 if(search_wait){if(!--search_wait){++round_no;search_round();}return;}
 if(travel_lock)--travel_lock;
 if(!travel_lock&&!(pad&B)){
  if((pad&LEFT)&&cursor_x==8&&(district&1)){travel(district-1,228,cursor_y);return;}
  if((pad&RIGHT)&&cursor_x==232&&!(district&1)&&district_count>1){travel(district+1,12,cursor_y);return;}
  if((pad&UP)&&cursor_y==72&&district>=2){travel(district-2,cursor_x,200);return;}
  if((pad&DOWN)&&cursor_y==204&&district_count==4&&district<2){travel(district+2,cursor_x,76);return;}
 }
 if((pad&LEFT)&&cursor_x>8){cursor_x=cursor_x<8+speed?8:cursor_x-speed;moved=1;}
 if((pad&RIGHT)&&cursor_x<232){cursor_x=cursor_x>232-speed?232:cursor_x+speed;moved=1;}
 if((pad&UP)&&cursor_y>72){cursor_y=cursor_y<72+speed?72:cursor_y-speed;moved=1;}
 if((pad&DOWN)&&cursor_y<204){cursor_y=cursor_y>204-speed?204:cursor_y+speed;moved=1;}
 if(moved)hover_npc=cursor_person();
 if((pressed&A)&&!feedback){
  feedback_x=hover_npc<24?npc_x[hover_npc]:cursor_x;
  feedback_y=hover_npc<24?npc_y[hover_npc]:cursor_y;
  if(target<24&&hover_npc==target){++found;attempt_score+=500+seconds*10;feedback=40;sound(1);hud_dirty=1;
   if(found==3){finish(1);return;}search_wait=45;return;
  }else{++misses;feedback=30;sound(2);seconds=seconds>5?seconds-5:0;hud_dirty=1;if(!seconds){finish(0);return;}}
 }
 if(++tick==60){tick=0;hud_dirty=1;if(seconds)--seconds;if(!seconds)finish(0);}
}
void draw(void){u8 i,x,y,step;hide();sprite_bank=96;
 /* NMI applies the requested frame atomically in vblank. No tile uploads in play. */
 if(mode==HUB||mode==ENDING||mode==RESULT)art_bank=(anim_tick&31)<5?(anim_tick>>5)&3:0;
 else if(mode==REPAIR)art_bank=4+((anim_tick>>4)&3);
 else if(mode==RHYTHM)art_bank=8+((song_step>>1)&3);
 else art_bank=scene_bank+((anim_tick>>4)&3);
 if(mode==HUB||mode==ENDING){
  if(mode==HUB){x=32+host*64;
   sprite(x,120,48,3);sprite(x+56,120,49,3);
   sprite(x,176,50,3);sprite(x+56,176,51,3);
  }
  for(i=0;i<3;++i)if(completed&masks[i])sprite(84+i*64,184,39,3);
  if(mode==ENDING){for(i=0;i<8;++i)sprite(24+i*28,40+((anim_tick+i*23)%80),SPARK,3);}return;
 }
 if(mode==RESULT){sprite(24,112,last_win?39:CROSS,3);
  for(i=0;i<3;++i)sprite(104+i*16,100,i<result_grade?MEDAL:40,3);
  return;
 }
 if(mode==REPAIR){
  if(task_active){task_draw();return;}
  step=((pad&15)?((walk>>3)&1):0)+(facing?2:0);
  for(i=0;i<12;++i)sprite(px-4+hero_dx[i],py-8+hero_dy[i],188+step*12+i,0);
  if(studio_stun||(feedback&&flash==4))sprite(px+4,py-17,CROSS,3);
  /* The table occludes their legs, so they sit behind the equipment. */
  for(i=0;i<4;++i){
   sprite(96+(i&1)*8,94+(i>>1)*8,12+i,1);
   sprite(144+(i&1)*8,94+(i>>1)*8,24+i,2);
  }
  for(i=0;i<5;++i)sprite(176+i*9,208,i<health?HEART:EMPTY_HEART,3);
  for(i=0;i<4;++i){
   if(alarm[i]){
    if(alarm[i]>3||(frame&8))sprite(sx[i]-4,sy[i]-30,36,3);
    sprite(sx[i]-4,sy[i]-20,alarm[i]>8?40:(alarm[i]>4?240:241),3);
    sprite(sx[i]+12,sy[i]-25,42,3);
   }else if(feedback&&flash==i){
    sprite(sx[i]-4,sy[i]-30,39,3);
    sprite(sx[i]-15,sy[i]-12-(feedback>>3),SPARK,3);
    sprite(sx[i]+9,sy[i]+2+(feedback>>3),SPARK,3);
   }
  }
  if(cheer)sprite(120,208,MEDAL,3);
  if(!cooldown)sprite(232,190,38,0);
 }else if(mode==RHYTHM){
  x=116;y=94;
  if(feedback){if(pose==2)x-=12;else if(pose==3)x+=12;else if(pose==4)y-=10;else if(pose==5)y+=5;}
  step=feedback?(pose==6?0:(pose==2?2:(pose==3?3:1))):((song_step&2)?0:1);
  for(i=0;i<5;++i)sprite(88+i*16,72,rhythm_chain>i?(cheer?MEDAL:SPARK):40,3);
  for(i=0;i<15;++i)sprite(x+hero_dx[i],y+hero_dy[i],hero_base[step]+i,i<6?0:1);
  if(feedback){sprite(x-12,y+20,pose==6?CROSS:SPARK,3);sprite(x+28,y+20,pose==6?CROSS:SPARK,3);}
  if(cue_demo){token(60,0);if(frame&16)sprite(60,155,41,3);}
  else{
   for(i=0;i<3;++i)if(note_live[i])token(240-note_age[i]*2,note_key[i]);
   if(count_in)sprite(120,176,52+(120-count_in)/30,3);
  }
  if(feedback&&pose<6){
   if(judgement){for(i=0;i<5;++i)sprite(108+i*8,80,180+i,3);}
   else{sprite(112,80,180,3);sprite(120,80,185,3);sprite(128,80,186,3);sprite(136,80,187,3);}
  }
  for(i=0;i<4;++i)sprite(100+i*16,154,(beat_flash&&i==beat_no)?39:40,3);
  if(beat_flash){sprite(48,166,48,3);sprite(73,166,49,3);sprite(48,187,50,3);sprite(73,187,51,3);}
 }else if(mode==SEARCH){
  /* Small map and edge arrows explain the connected plaza without a text wall. */
  for(i=0;i<district_count;++i)sprite(8+(i&1)*10,32+(i>>1)*10,i==district?39:((visited&(1<<i))?SPARK:40),3);
  /* Birds remain above the crowd; the horizontal cart has been removed. */
  if(round_no&&!(pad&B)){x=anim_tick;if(x>=224)x-=224;
   sprite(232-x,84,60+((anim_tick>>3)&1),0);
   sprite(216-(anim_tick>>1),76,60+((anim_tick>>3)&1),0);
  }
  person(120,24,2,0);x=cursor_x;y=cursor_y;
  if(hover_npc<24)focus(npc_x[hover_npc]-2,npc_y[hover_npc],35);
  else focus(x-2,y-3,3);
  if(feedback){
   y=feedback_y-10-((40-feedback)>>3);
   if(search_wait)sprite(feedback_x+4,y,39,3);
   else{sprite(feedback_x,y,253,3);sprite(feedback_x+8,y,DIGITS+5,3);}
  }
  zoom_npc=255;
  if((pad&B)&&hover_npc<24){
   zoom_npc=hover_npc;sprite_bank=100;x=cursor_x<128?208:16;y=48;
   for(i=0;i<4;++i)sprite(x+i*8,y-8,56+i,3);
   for(i=0;i<16;++i)sprite(x+(i&3)*8,y+(i>>2)*8,64+crowd[zoom_npc]*16+i,2);
  }
 }
}
void main(void){mode=HUB;host=0;completed=0;rng=91;score=0;best=0;previous_target=255;music_track=255;bg_bank=0;sprite_bank=96;
 off();chr_bank(0);load_palette(palette,32);REG(0x4015)=0x0f;REG(0x4001)=0;REG(0x4005)=0;hub();
 for(;;){
  if(!paused)++anim_tick;draw();wait_frame();oldpad=pad;pad=pad_read();pressed=pad&~oldpad;
  if(mode==HUB){
   audio();random();
   if(pressed&(RIGHT|SELECT)){host=(host+1)%3;menu_selection();sound(1);}
   else if(pressed&LEFT){host=host?host-1:2;menu_selection();sound(1);}
   else if(pressed&(START|A)){if(!(completed&masks[host]))start_game();else sound(2);}
  }else if(mode>=REPAIR&&mode<=SEARCH){
   if(pressed&START){paused=!paused;if(paused)silence();else music_restore=1;hud_update();continue;}
   if(paused){if(pressed&B)hub();else if(pressed&A)start_game();continue;}
   audio();if(feedback)--feedback;if(cheer)--cheer;
   if(mode==REPAIR){studio_step();if(mode==REPAIR&&++tick==60){tick=0;
    if(task_active){hud_dirty=1;if(!--seconds){task_active=0;finish(0);}}else repair_second();}}
   else if(mode==RHYTHM)rhythm_step();
   else search_step();
   if(mode>=REPAIR&&mode<=SEARCH&&hud_dirty)hud_update();
  }else if(mode==RESULT){
   audio();if(last_win){if(pressed&(A|B|START))hub();}
   else if(pressed&B)hub();else if(pressed&(A|START))start_game();
  }else if(mode==ENDING){audio();if(pressed&START){completed=0;score=0;host=0;hub();}}
 }
}
