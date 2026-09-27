#include "adventure.h"
/* Fixed-capacity simulation. Static screens keep collision, pause and cues stable
   on the handheld; connected rooms provide height and changing routes. */
u8 adv_bank,adv_service_op,adv_service_arg,adv_ui_page,adv_command,adv_ui_sel;
u8 adv_trial,adv_code[12],adv_code_error,adv_activity_result,adv_task_fails,adv_password_load;
u8 adv_sprite_tail,adv_sprite_actor;
AdvSave adv_save;
AdvState adv;
const Platform layouts[20][5]={
 {{0,208,80,0},{88,176,48,0},{144,144,48,0},{200,176,56,0},{48,128,32,0}},
 {{0,208,96,0},{72,168,56,0},{144,128,48,0},{208,168,48,0},{144,208,48,0}},
 {{0,192,64,0},{80,152,48,0},{144,184,48,0},{208,144,48,0},{32,112,32,0}},
 {{0,208,64,0},{72,168,32,1},{136,136,56,0},{208,176,48,0},{32,128,32,0}},
 {{0,208,128,0},{64,160,48,0},{144,128,48,0},{128,208,128,0},{0,0,0,0}},
 {{0,208,80,0},{80,160,48,2},{152,112,48,0},{208,160,48,0},{16,128,32,0}},
 {{0,192,56,0},{64,160,48,0},{128,192,48,0},{192,160,64,0},{144,120,32,0}},
 {{0,208,128,0},{48,160,48,0},{152,160,48,0},{128,208,128,0},{0,0,0,0}},
 {{0,208,72,0},{80,176,48,0},{144,152,48,0},{208,192,48,0},{40,136,32,0}},
 {{0,192,72,0},{88,152,48,0},{152,120,48,0},{208,160,48,0},{24,112,32,0}},
 {{0,208,80,0},{88,184,40,0},{144,152,56,0},{208,184,48,0},{56,120,32,0}},
 {{0,192,80,0},{88,160,48,0},{152,192,40,0},{208,152,48,0},{40,120,32,0}},
 {{0,208,96,0},{88,160,48,0},{152,136,48,0},{208,176,48,0},{32,128,32,0}},
 {{0,208,72,0},{80,168,48,2},{144,120,48,0},{208,168,48,0},{32,120,32,0}},
 {{0,192,64,0},{72,160,56,0},{144,128,48,0},{208,168,48,0},{16,112,32,0}},
 {{0,208,88,0},{96,176,40,0},{152,144,48,0},{208,192,48,0},{48,128,32,0}},
 {{0,192,80,0},{88,144,48,0},{152,176,48,0},{208,144,48,0},{32,104,32,0}},
 {{0,208,80,0},{80,176,48,0},{144,136,48,0},{208,176,48,0},{32,128,32,0}},
 {{0,208,96,0},{96,168,48,0},{160,136,40,0},{208,176,48,0},{48,120,32,0}},
 {{0,208,128,0},{56,160,48,0},{144,128,48,0},{128,208,128,0},{16,128,32,0}}
};
const u8 room_layout[9][16]={
 {0,6,1,8,2,9,10,11,3,12,13,14,15,16,17,19},
 {3,1,5,8,6,9,10,11,12,13,14,15,16,17,18,7},
 {4,0,6,8,1,9,10,11,12,14,15,16,17,18,19,4},
 {1,4,8,9,0,10,11,12,14,15,16,17,18,19,2,7},
 {19,0,8,9,1,6,10,11,12,2,14,15,16,17,18,4},
 {19,6,8,9,1,0,10,11,12,2,14,15,16,17,18,7},
 {4,6,0,8,3,9,10,11,12,14,19,7},
 {2,3,6,8,5,9,10,11,12,13,18,7},
 {0,5,8,9,4,10,11,12,2,14,19,7}
};
const u8 stage_world[9]={0,0,1,1,2,2,3,4,0};
const u8 stage_rooms[9]={16,16,16,16,16,16,12,12,12};
const u8 stage_music[5]={11,12,13,14,15};

static void service(u8 op,u8 arg){adv_service_op=op;adv_service_arg=arg;adv_service();}
static void screen(u8 page){adv_ui_page=page;adv_present();}
static u8 ypixel(void){return (u8)(adv.y>>4);}
static u8 distance(u8 a,u8 b){return a>b?a-b:b-a;}
static u8 mystery(void){return adv.stage==4||adv.stage==5;}
static u8 relay_mask(void){return adv.stage==2?(adv.room<4?4:(adv.room<8?6:7)):7;}
static u8 boss_room(void){return adv.room==stage_rooms[adv.stage]-1&&(adv.stage&1||adv.stage>=6);}
/* At most 47 sprites: use the fixed-bank OAM writer shared with the classic game. */
#define sprite8 sprite
#define shape adv_shape
static void hud_line(void){u8 i;const char* hint;
 for(i=0;i<32;++i){hud[i]=32;status_row[i]=32;}
 hud[1]='T';hud[2]='O';hud[3]='M';hud[4]='A';hud[6]='1'+adv.stage;
 hud[9]='S';hud[10]='A';hud[11]='L';hud[12]='A';hud[13]='0'+(adv.room+1)/10;hud[14]='0'+(adv.room+1)%10;hud[15]='/';hud[16]='0'+stage_rooms[adv.stage]/10;hud[17]='0'+stage_rooms[adv.stage]%10;
 hud[21]='V';hud[22]='I';hud[23]='D';hud[24]='A';hud[26]='0'+adv.health;
 if(adv_save.easy){hud[28]='+';}
 hint=adv.room==0&&adv.stage==0?"A:SALTA B:ACCION ARRIBA:USA":(adv.keys?"ARRIBA: PUERTA DE SALIDA":"ARRIBA: ACTIVA LA CLAQUETA");
 if(boss_room())hint=adv.boss_hp?"ESQUIVA Y ESPERA EL DESCANSO":"TOMA LISTA! VE A LA SALIDA";
 if(adv.world==1&&!adv.keys&&!boss_room())hint="B: APAGA EL REPETIDOR";
 if(adv.world==3&&!adv.keys&&!boss_room())hint="LISTA: 0/3 BUSCA ENCARGOS";
 if(adv.world==4&&!adv.keys&&!boss_room())hint="PAJARITO VUELA. BOCINA TIRA.";
 if(mystery())hint=adv.room==0?"ARRIBA: ELIGE UNA RUTA":(adv.room<=12&&!(adv.room&3)?"ARRIBA: HABLAR CON EL EQUIPO":(adv.keys?"SELECT: MAPA Y LIBRETA":"ARRIBA: LEE LA PISTA"));
 if(boss_room()&&adv.boss_hp){
  if(adv.world==1)hint=adv.boss_tick>=100?"RECARGANDO! AHORA ATACA":(adv.boss_round==0?"AVISO: RAFAGA BAJA. SALTA!":(adv.boss_round==1?"AVISO: DIAGONAL. BUSCA HUECO":"AVISO: ECO DESDE ARRIBA"));
  if(adv.world==2)hint=adv.boss_tick>=100?((adv.boss_marks&(1<<adv.boss_round))?"SELLO LISTO. ESPERA EL OTRO":"RECARGA: ARRIBA LEE EL SELLO"):(adv.boss_round==0?"SELLO PALTA: ONDA DIAGONAL":(adv.boss_round==1?"SELLO FRUTILLA: LLUVIA":"SELLO CHOCLO: ONDA BAJA"));
 }
 if(adv.flash)hint="CINTA ENCONTRADA! YA ES TUYA";
 for(i=0;i<28&&hint[i];++i)status_row[i+2]=hint[i];
 adv.hud_state=adv.keys|(adv.flash?2:0)|(adv.props<<2);
 if(boss_room()){for(i=8;i<18;++i)hud[i]=32;hud[8]=adv.world==2?'S':'J';hud[9]='E';hud[10]=adv.world==2?'L':'F';hud[11]=adv.world==2?'L':'E';if(adv.world==2)hud[12]='O';hud[13]='0'+adv.boss_hp;}
 if(adv.world==3&&!boss_room()&&!adv.keys)status_row[9]='0'+(adv.props&1)+((adv.props>>1)&1)+((adv.props>>2)&1);
 hud_on=1;
}
static void load_room(u8 entrance){u8 i,layout;Platform* p;Enemy* e;
 adv.world=adv.stage==8?adv.room/4:stage_world[adv.stage];
 layout=room_layout[adv.stage][adv.room];
 for(i=0;i<5;++i)adv.platforms[i]=layouts[layout][i];
 /* Leave the boss approach open: the old right ledge caught evasive jumps
    directly above melee range, forcing a blind drop onto the boss. */
 if(boss_room()){adv.platforms[2].x=88;adv.platforms[2].y=128;}
 if(adv.world==0&&adv.room>=3&&adv.platforms[1].kind==0)adv.platforms[1].kind=2;
 adv.exit_y=adv.platforms[3].y-24;
 adv.gate_x=adv.platforms[2].x+12;adv.gate_y=adv.platforms[2].y-16;
 if(adv.world==2){adv.gate_x=adv.platforms[1].x+12;adv.gate_y=adv.platforms[1].y-16;}
 adv.tape_x=adv.platforms[4].w?adv.platforms[4].x+8:adv.platforms[2].x+16;
 adv.tape_y=(adv.platforms[4].w?adv.platforms[4].y:adv.platforms[2].y)-16;
 adv.tape=adv.stage<8&&adv.room==(mystery()?3:4)&&!(adv_save.tapes&(1<<adv.stage));
 adv.flags[adv.room]|=128;
 adv.keys=adv.flags[adv.room]&1;adv.boss_hp=boss_room()?(adv.world==2?3:(adv_save.easy?4:6)):0;
 adv.bridge_width=adv.platforms[3].w;
 if(adv.world==1&&!boss_room()){
  adv.keys=(adv.flags[adv.room]&relay_mask())==relay_mask();
  if(!adv.keys)adv.platforms[3].w=0;
 }
 if(mystery()&&!boss_room()){
  adv.keys=adv.room&&((adv.room&3)!=0)&&!(adv.stage==5&&((adv.room&3)==2||adv.room>=13));
  if(adv.flags[adv.room]&1)adv.keys=1;
  if(adv.room&&adv.room<=12&&!(adv.room&3))adv.keys=0;
 }
 adv.boss_round=adv.boss_marks=0;
 adv.boss_tick=adv.boss_inv=0;adv.boss_x=176;adv.boss_y=184;adv.props=0;adv.vy=0;adv.ground=1;adv.coyote=5;
 adv.x=entrance?216:16;adv.y=((u16)(entrance?adv.exit_y:adv.platforms[0].y-24))<<4;
 adv.attack=adv.cooldown=adv.buffer=adv.dead=adv.hitstop=adv.flash=0;
 adv.run_phase=adv.landing=adv.hurt=0;
 adv.inv=45;adv.tick=0;adv.facing=entrance;adv.clue=0;
 if(adv.world==1&&!boss_room())adv.props=adv.flags[adv.room]&7;
 if(adv.world==3&&adv.keys)adv.props=7;
 if(adv.world==2&&boss_room()){adv.gate_x=112;adv.gate_y=192;}
 if(mystery()&&(!adv.room||(adv.room<=12&&!(adv.room&3)))){adv.gate_x=adv.platforms[0].x+40;adv.gate_y=adv.platforms[0].y-16;}
 for(i=0;i<BCOUNT;++i)adv.bullets[i].life=0;
 for(i=0;i<ECOUNT;++i){
  e=&adv.enemies[i];e->hp=0;
  if(boss_room()||(mystery()&&(!adv.room||(adv.room<=12&&!(adv.room&3))))||i>1||(adv.stage==0&&(adv.room<2||i>0))||(adv_save.easy&&i>0))continue;
  p=&adv.platforms[i+1];e->lo=p->x;e->hi=p->x+p->w-16;e->x=e->hi;e->y=p->y-16;
  e->type=(adv.world*2+i+adv.room)%6;e->hp=adv_save.easy?1:2;e->tick=i*53;e->inv=0;e->dir=-1;
 }
 if((mystery()?(!adv.room||(adv.room&1)):((adv.room&1)==0))||boss_room()){
  if(adv.room!=adv.checkpoint)adv.health=adv_save.easy?6:4;adv.checkpoint=adv.room;
 }
 screen(UI_ROOM);hud_line();
 service(5,stage_music[adv.world]);
}
/* Animation clocks follow actual grounded movement. Facing is applied to both
   tile order and pixels, so limbs and the direction of the action agree. */
static u8 actor_pose(void){
 if(adv.hurt>78)return 15;
 if(adv.attack)return adv.attack>11?12:(adv.attack>5?13:14);
 if(!adv.ground)return adv.vy<-20?8:(adv.vy>24?10:9);
 if(adv.landing)return 11;
 if(adv.run_phase)return 2+((adv.run_phase-1)>>2);
 return (adv.tick&127)>=124?1:0;
}
static void draw(void){u8 i,pose,legs,y,flip;Enemy* e;Bullet* b;Platform* p;
 hide();art_bank=54+adv.world;sprite_bank=59*4;adv_sprite_tail=244+adv.world;
 adv_sprite_actor=host==0?236:(host==1?252:254);
 y=ypixel();pose=actor_pose();legs=pose;flip=adv.facing?64:0;
 /* Keep the stride/jump underneath an upper-body action. Holding B must not
    turn running into a sliding, frozen full-body attack pose. */
 if(adv.attack&&adv.hurt<=78){
  if(!adv.ground)legs=adv.vy<-20?8:(adv.vy>24?10:9);
  else if(adv.run_phase)legs=2+((adv.run_phase-1)>>2);
  else if(adv.landing)legs=11;
 }
 if(!adv.hurt||adv.hurt>78||(adv.hurt&2)){
  shape(adv.x,y-8,pose*8,2,2,flip);
  shape(adv.x,y+8,pose*8+4,2,1,1|flip);
  shape(adv.x,y+16,legs*8+6,2,1,2|flip);
  if(pose==13)shape(adv.facing?adv.x-8:adv.x+16,y+4,128+host*2,1,2,flip);
 }
 if(!adv.keys&&!boss_room()&&adv.world!=3&&adv.world!=1&&!(mystery()&&(!adv.room||(adv.room<=12&&!(adv.room&3)))))sprite8(adv.gate_x,adv.gate_y,158,3);
 if(adv.tape)sprite8(adv.tape_x+4,adv.tape_y+4-((adv.tick>>4)&1),154,3);
 if(boss_room()&&adv.boss_hp&&(!adv.boss_inv||(adv.boss_inv&2))){
  shape(adv.boss_x+4,adv.boss_y,216+(adv.boss_tick<45?0:(adv.boss_tick<85?18:9)),2,3,3);

 }
 if(adv.world==3&&!boss_room())for(i=0;i<3;++i)if(!(adv.props&(1<<i))){p=&adv.platforms[i+1];sprite8(p->x+12,p->y-12,159,3);}
 for(i=0;i<5;++i)if(adv.platforms[i].kind==1){
  sprite8(adv.platforms[i].x,adv.platforms[i].y,164,3);sprite8(adv.platforms[i].x+8,adv.platforms[i].y,165,3);
  sprite8(adv.platforms[i].x+16,adv.platforms[i].y,164,3);sprite8(adv.platforms[i].x+24,adv.platforms[i].y,165,3);
 }
 for(i=0;i<ECOUNT;++i){e=&adv.enemies[i];if(e->hp&&(!e->inv||(e->inv&2)))shape(e->x,e->y,168+e->type*8+((e->type==1||e->type==4)?(e->tick>=80&&e->tick<100):((e->tick>>4)&1))*4,2,2,3|(e->dir<0?64:0));}
 for(i=0;i<BCOUNT;++i){b=&adv.bullets[i];if(b->life)sprite8(b->x,b->y,160,b->owner?0:3);}
}
static u8 attack_hits(u8 x,u8 y,u8 width);
static void relay(u8 x,u8 y,u8 width){u8 j;Platform* p;
 for(j=0;j<3;++j){p=&adv.platforms[j];
  if(!(relay_mask()&(1<<j))||(adv.props&(1<<j)))continue;
  if((width?attack_hits(p->x+16,p->y-16,8):(distance(x,p->x+20)<12&&distance(y,p->y-12)<14))){
   adv.props|=1<<j;adv.flags[adv.room]|=1<<j;
   if((adv.props&relay_mask())==relay_mask()){adv.keys=1;adv.platforms[3].w=adv.bridge_width;}
   service(2,1);screen(UI_RELAY);return;
  }
 }
}
static void damage(void){
 if(adv.inv||adv.dead)return;
 adv.damaged=1;adv.inv=90;adv.hurt=90;adv.hitstop=4;
 adv.attack=0;adv.cooldown=12;
 if(adv.ground){adv.vy=-36;adv.ground=0;}
 if(adv.health)--adv.health;
 service(2,2);
 if(!adv.health)adv.dead=1;
}
static void shoot(u8 x,u8 y,s8 vx,s8 vy,u8 owner){u8 i;
 for(i=0;i<BCOUNT;++i)if(!adv.bullets[i].life){adv.bullets[i].x=x;adv.bullets[i].y=y;adv.bullets[i].vx=vx;adv.bullets[i].vy=vy;adv.bullets[i].owner=owner;adv.bullets[i].life=70;break;}
}
static u8 attack_hits(u8 x,u8 y,u8 width){s16 a,b;
 if(adv.attack>11||adv.attack<6||distance(ypixel()+12,y+8)>20)return 0;
 a=adv.facing?(s16)adv.x-14:adv.x+10;b=adv.facing?adv.x+6:adv.x+30;
 return b>x&&a<(s16)x+width;
}
static void enemies(void){u8 i,py;Enemy* e;Bullet* b;s16 x,y;
 py=ypixel();
 for(i=0;i<ECOUNT;++i){
  e=&adv.enemies[i];if(!e->hp)continue;
  ++e->tick;if((e->type==2||e->type==5))e->y=adv.platforms[i+1].y-16-((e->tick&63)<32?(e->tick&31)/2:(63-(e->tick&63))/2);if(e->inv)--e->inv;
  if((e->type==1||e->type==4)){
   if(e->tick==100)shoot(e->x,e->y+4,e->x>adv.x?-2:2,adv.world==1&&e->type==4?1:0,0);
   if(e->tick>=140)e->tick=0;
  }else if(!(e->tick&1)){
   if(e->x<=e->lo)e->dir=1;if(e->x>=e->hi)e->dir=-1;
   e->x+=e->dir;
  }
  if(attack_hits(e->x,e->y,16)&&!e->inv){--e->hp;e->inv=18;adv.hitstop=2;service(2,e->hp?3:1);}
  if(e->hp&&adv.x+12>e->x&&adv.x+3<e->x+14&&py+24>e->y&&py<e->y+14){
   if(adv.vy>0&&py+16<e->y){--e->hp;e->inv=18;adv.vy=-64;adv.ground=0;service(2,1);}
   else damage();
  }
 }
 for(i=0;i<BCOUNT;++i){
  b=&adv.bullets[i];if(!b->life)continue;
  x=(s16)b->x+b->vx;y=(s16)b->y+b->vy;
  if(x<4||x>248||y<48||y>228){b->life=0;continue;}
  b->x=(u8)x;b->y=(u8)y;--b->life;
  if(!b->owner&&host==2&&attack_hits(b->x,b->y,8)){b->owner=1;b->vx=-b->vx;b->vy=0;service(2,1);}
  if(!b->owner&&distance(adv.x+8,b->x)<12&&distance(py+12,b->y)<16){damage();b->life=0;}
  if(b->owner){
   for(py=0;py<ECOUNT;++py){e=&adv.enemies[py];if(e->hp&&!e->inv&&distance(e->x+8,b->x)<12&&distance(e->y+8,b->y)<12){--e->hp;e->inv=18;b->life=0;service(2,1);break;}}
   if(adv.world==1&&!boss_room()&&!adv.keys){relay(b->x,b->y,0);}
   if(boss_room()&&adv.world!=2&&adv.boss_hp&&adv.boss_tick>=100&&!adv.boss_inv&&distance(adv.boss_x+12,b->x)<20&&distance(adv.boss_y+12,b->y)<20){adv.boss_hp=adv.boss_hp>1?adv.boss_hp-2:0;adv.boss_inv=20;b->life=0;service(2,1);}
  }
  py=ypixel();
 }
 if(boss_room()&&adv.boss_hp){
  if(adv.boss_inv)--adv.boss_inv;
  if(++adv.boss_tick>=180){adv.boss_tick=0;adv.boss_round=(adv.boss_round+1)%3;}
  adv.boss_x=176;adv.boss_y=184;
  if(adv.world==0){
   if(adv.boss_tick==45||adv.boss_tick==70)shoot(adv.x+8,64,0,3,0);
  }else if(adv.world==1){
   if(adv.boss_tick==50||adv.boss_tick==75){
    if(adv.boss_round==0)shoot(176,192,-3,0,0);
    else if(adv.boss_round==1)shoot(176,152,-2,1,0);
    else shoot(adv.x+8,64,0,3,0);
   }
  }else if(adv.world==2){
   if(adv.boss_tick<100)adv.boss_y=144;
   if(adv.boss_tick==50||adv.boss_tick==80){
    if(adv.boss_round==0)shoot(176,152,-2,1,0);
    else if(adv.boss_round==1)shoot(adv.x+8,64,0,3,0);
    else shoot(176,192,-3,0,0);
   }
  }else if(adv.world==3){
   if(adv.boss_tick>=45&&adv.boss_tick<100)adv.boss_x=176-(adv.boss_tick-45);
   if(adv.boss_tick==40)shoot(176,192,-2,0,0);
  }else{
   if(adv.boss_tick<100)adv.boss_y=144;
   if(adv.boss_tick==45||adv.boss_tick==75)shoot(adv.x+8,80,0,3,0);
  }
  if(adv.world!=2&&adv.boss_tick>=100&&attack_hits(adv.boss_x,adv.boss_y,24)&&!adv.boss_inv){
   --adv.boss_hp;adv.boss_inv=20;adv.hitstop=3;service(2,1);
  }
  if(adv.x+12>adv.boss_x&&adv.x<adv.boss_x+22&&py+22>adv.boss_y&&py<adv.boss_y+22)damage();
 }
 if(boss_room()&&!adv.boss_hp&&!adv.keys){adv.keys=1;adv.flags[adv.room]|=1;for(i=0;i<BCOUNT;++i)adv.bullets[i].life=0;}
}
static void physics(void){u8 i,py,landed,nx;Platform* p;s16 next,top;
 for(i=0;i<5;++i){p=&adv.platforms[i];if(p->kind==1){
  nx=72+((adv.tick&63)<32?(adv.tick&31)/2:(63-(adv.tick&63))/2);
  if(adv.ground&&ypixel()+24==p->y&&adv.x+12>p->x&&adv.x<p->x+p->w)adv.x+=nx-p->x;
  p->x=nx;
 }}
 if(adv.hurt)--adv.hurt;if(adv.landing)--adv.landing;
 if(adv.inv)--adv.inv;if(adv.cooldown)--adv.cooldown;if(adv.attack)--adv.attack;
 if(adv.buffer)--adv.buffer;if(adv.coyote)--adv.coyote;
 if(pressed&A)adv.buffer=6;
 if(pad&LEFT){adv.facing=1;if(adv.x>9)adv.x-=2;}
 else if(pad&RIGHT){adv.facing=0;if(adv.x<230)adv.x+=2;}
 if(adv.ground&&(pad&(LEFT|RIGHT))&&adv.x>9&&adv.x<230){
  if(++adv.run_phase>24)adv.run_phase=1;
 }else adv.run_phase=0;
 if((pad&B)&&!adv.cooldown&&adv.hurt<=78){adv.attack=14;adv.cooldown=host==1?28:20;
 }
 if(adv.attack==11){
  if(host==1)shoot(adv.facing?adv.x-4:adv.x+16,ypixel()+8,adv.facing?-3:3,0,1);
  service(2,3);
 }
 if(adv.buffer&&adv.coyote){adv.vy=-94;
  for(i=0;i<5;++i){p=&adv.platforms[i];if(p->kind==2&&ypixel()+24==p->y&&adv.x+12>p->x&&adv.x<p->x+p->w)adv.vy=-112;}adv.ground=adv.coyote=adv.buffer=0;service(2,4);}
 if(!(pad&A)&&adv.vy<-36)adv.vy=-36;
 adv.vy+=5;if(adv.vy>80)adv.vy=80;
 next=adv.y+adv.vy;landed=0;
 if(adv.vy>=0){
  for(i=0;i<5;++i){p=&adv.platforms[i];if(!p->w)continue;
   top=((s16)p->y-24)<<4;
   if(adv.x+12>p->x&&adv.x+3<(u16)p->x+p->w&&adv.y<=top+4&&next>=top){
    next=top;adv.vy=0;landed=1;break;
   }
  }
 }
 if(next<48*16){next=48*16;if(adv.vy<0)adv.vy=0;}
 if(landed&&!adv.ground)adv.landing=5;
 adv.y=next;adv.ground=landed;if(landed)adv.coyote=5;
 if(next>232*16){adv.damaged=1;adv.dead=1;service(2,2);}
 py=ypixel();
 if(adv.tape&&distance(adv.x+8,adv.tape_x+8)<16&&distance(py+12,adv.tape_y+8)<20){
  adv.tape=0;adv_save.tapes|=1<<adv.stage;adv.flash=90;service(2,1);
 }
 if(adv.world==1&&!boss_room()&&!adv.keys&&adv.attack)relay(0,0,1);
 if(adv.world==3&&!boss_room()){
  for(i=0;i<3;++i){p=&adv.platforms[i+1];if(!(adv.props&(1<<i))&&distance(adv.x+8,p->x+16)<20&&distance(py+12,p->y-8)<20){adv.props|=1<<i;service(2,1);}}
  if(adv.props==7){adv.keys=1;adv.flags[adv.room]|=1;}
 }
 if((pressed&UP)&&!adv.keys&&adv.world!=1&&adv.world!=3&&distance(adv.x+8,adv.gate_x+4)<22&&distance(py+12,adv.gate_y+4)<24){
  if(boss_room()){
   if(adv.world==2&&adv.boss_tick>=100){
    adv.clue=adv.boss_round;
    if(!(adv.boss_marks&(1<<adv.clue))){
     screen(UI_CLUE);if(adv_command==1){adv.boss_marks|=1<<adv.clue;--adv.boss_hp;adv.boss_inv=20;service(2,1);}
     screen(UI_ROOM);hud_line();adv_command=10;
    }
   }
  }else if(mystery()&&!adv.room){
   screen(UI_ROUTES);adv_command=adv_command?adv_command+30:34;return;
  }else if(mystery()&&adv.room<=12&&!(adv.room&3)){
   adv.clue=adv.room/4-1;screen(UI_NPC);
   adv.flags[adv.room]|=1;adv_command=30;return;
  }else{
   if(adv.world==2){
    adv.clue=adv.room>=13?(adv.room-13)%3:((adv.room-1)/4)%3;
    screen(UI_CLUE);if(adv_command!=1){screen(UI_ROOM);adv_command=10;return;}screen(UI_ROOM);adv_command=10;
   }
   adv.keys=1;adv.flags[adv.room]|=1;service(2,1);
  }
 }
 if(adv.flash)--adv.flash;
}
static u8 unlocked(u8 stage){
 if(stage<2)return stage==0||(adv_save.cleared&1);
 if(stage<4)return (adv_save.cleared&3)==3&&(stage==2||(adv_save.cleared&4));
 if(stage<6)return (adv_save.cleared&15)==15&&(stage==4||(adv_save.cleared&16));
 return (adv_save.cleared&63)==63&&(stage!=8||adv_save.tasks==7);
}
static void stage_start(u8 stage){u8 i;
 adv.stage=stage;adv.room=adv.checkpoint=adv.damaged=adv.room_seen=adv.death_count=0;adv.health=adv_save.easy?6:4;
 adv.helped=adv_save.easy;for(i=0;i<MAX_ROOMS;++i)adv.flags[i]=0;
 screen(UI_INTRO);if(adv_command==0)return;
 load_room(0);adv_command=10;
}
static void stage_done(void){
 adv_save.cleared|=(u16)1<<adv.stage;
 if(!adv.damaged&&!adv.helped&&!adv_save.easy)adv_save.perfect|=(u16)1<<adv.stage;
 service(1,4);screen(UI_RESULT);
 if((adv.stage&1)||adv.stage>=6)screen(adv.stage==8?UI_ENDING:UI_OUTRO);
 adv_command=0;
}
static void play(void){u8 cmd;
 while(adv_command==10){
  draw();wait_frame();oldpad=pad;pad=pad_read();pressed=pad&~oldpad;
  if(pressed&START){
   paused=1;service(3,0);screen(UI_PAUSE);cmd=adv_command;
   if(cmd==2){adv.room=adv.checkpoint;adv.health=adv_save.easy?6:4;adv.damaged=1;load_room(0);}
   else if(cmd==3){paused=0;adv_command=0;return;}
   else if(cmd==4){adv_save.easy=!adv_save.easy;adv.helped=1;if(adv_save.easy&&adv.health<6)adv.health=6;}
   else if(cmd==5){adv_password_load=0;screen(UI_PASSWORD);}
   else if(cmd==6)screen(UI_HELP);
   paused=0;screen(UI_ROOM);service(5,stage_music[adv.world]);adv_command=10;continue;
  }
  if(adv.world==2&&(pressed&SELECT)){
   paused=1;service(3,0);screen(UI_BOOK);paused=0;screen(UI_ROOM);hud_line();service(5,stage_music[adv.world]);adv_command=10;continue;
  }
  if(mystery()&&adv.room&&(pressed&DOWN)&&adv.x<40&&adv.ground){adv.room=0;load_room(0);adv_command=10;continue;}
  service(0,0);++adv.tick;
  if(pressed&A)adv.buffer=6;
  if(adv.hitstop){--adv.hitstop;continue;}
  physics();
  if(adv_command>=30){
   cmd=adv_command;
   if(cmd!=34)adv.room=cmd==30?0:(cmd==35?13:1+(cmd-31)*4);
   if(cmd==34){screen(UI_ROOM);hud_line();}else load_room(0);adv_command=10;continue;
  }
  enemies();
  if(boss_room()&&(adv.boss_tick==0||adv.boss_tick==100))hud_line();
  if(adv.hud_state!=(adv.keys|(adv.flash?2:0)|(adv.props<<2)))hud_line();
  hud[26]='0'+adv.health;hud[28]=adv_save.easy?'+':32;if(boss_room())hud[13]='0'+adv.boss_hp;
  if(adv.dead){
   if(adv.death_count<255)++adv.death_count;
   screen(UI_FAILURE);
   if(adv_command==0){adv_command=0;return;}
   if(adv_command==2){adv_save.easy=1;adv.helped=1;}
   adv.health=adv_save.easy?6:4;adv.room=adv.checkpoint;load_room(0);adv_command=10;
  }
  if((pressed&UP)&&adv.keys&&adv.x>=212&&distance(ypixel(),adv.exit_y)<18){
   if(++adv.room==stage_rooms[adv.stage]){stage_done();return;}
   if(adv.room==(adv.stage<6?8:6)&&!(adv.room_seen&1)){adv.room_seen|=1;screen(UI_REWRITE);}
   load_room(0);adv_command=10;
  }
 }
}
static u8 prepare(u8 stage){u8 bit;
 if(stage>=6)return 1;bit=1<<(stage/2);
 if(adv_save.tasks&bit)return 1;
 adv.stage=stage;adv_task_fails=0;
 for(;;){
  screen(UI_TASK);
  if(!adv_command)return 0;
  if(adv_command==2){adv_save.tasks|=bit;return 1;}
  adv_activity_result=0;service(4,stage/2);mode=10;paused=0;
  if(adv_activity_result==1){adv_save.tasks|=bit;return 1;}
  if(adv_activity_result==2&&adv_task_fails<255)++adv_task_fails;
 }
}
void adv_main(void){u8 running,stage,root;running=1;root=1;
 mode=10;paused=0;adv_command=0;adv_ui_sel=adv_save.valid?0:1;
 service(1,0);
 while(running){
  if(root){
   screen(UI_ROOT);
   if(adv_command==4){running=0;continue;}
   if(adv_command==5){screen(UI_HELP);continue;}
   if(adv_command==3){adv_password_load=1;adv_code_error=0;screen(UI_PASSWORD);if(adv_command!=1)continue;}
   if(adv_command==2){
    if(adv_save.valid&&(adv_save.cleared||adv_save.tasks||adv_save.tapes)){screen(UI_CONFIRM);if(adv_command!=1)continue;}
    adv_save.valid=1;adv_save.cleared=adv_save.perfect=0;adv_save.tapes=adv_save.tasks=adv_save.easy=0;screen(UI_PROLOGUE);
   }
   if(!adv_save.valid)continue;
   root=0;adv_ui_sel=0;adv_trial=0;
  }
  service(1,0);screen(UI_STUDIO);
  if(adv_command==0){root=1;adv_ui_sel=0;continue;}
  if(adv_command==2){adv_password_load=0;screen(UI_PASSWORD);continue;}
  stage=adv_ui_sel<3?adv_ui_sel*2+adv_trial:adv_ui_sel+3;
  if(!unlocked(stage)){service(2,2);continue;}
  if(!prepare(stage))continue;
  stage_start(stage);if(adv_command==10)play();
  if(adv_ui_sel<3&&adv_save.cleared&((u16)1<<(adv_ui_sel*2)))adv_trial=1;
 }
 R(0x2000)=0;R(0x2001)=0;ready=0;hud_on=0;paused=0;mode=0;
}
