#include "adventure.h"
/* Banked UI owns static scene rendering and password encoding. The simulation
   stays in RAM while this 24 KiB window replaces the adventure code. */
const char* const anames[3]={"CHUCHO","ESTEFANIA","DANIEL"};
const char* const world_names[6]={"CHUCHO, BAJATE DE AHI","OPERACION: EL ESTOMAGO","EL HIJO DE LA CHILENA","NADIA: LA ULTIMA CAJA","EL CASTILLO DE APODOS","AHORA SI: EL SKETCH"};
const char* const level_names[9]={"UNA SUBIDITA TRANQUILA","RESCATE EXAGERADO","LA FABRICA DEL RUMOR","DEJENME TERMINAR!","DANIEL SABE LLEGAR","ESO NO VIENE CON MAPA","LA ULTIMA CAJA ABIERTA","EL CASTILLO DE LOS APODOS","ESTABAMOS GRABANDO!"};
const char* const intro[9][4]={
 {"CHUCHO: ES SUBIR Y YA.","ESTEFI: Y COMO BAJAS?","DANIEL: PONLE UNA ESCALERA.","SUBE HASTA EL MIRADOR."},
 {"CHUCHO: YA CASI LLEGAMOS.","DANIEL: TRAJE UN RESCATE.","ESTEFI: ESO ES UNA GRUA!","ESQUIVA LA AYUDA EXCESIVA."},
 {"ESTEFI: NO FUE OPERACION.","CHUCHO: MISION SECRETA?","DANIEL: LE PONGO ROBOTS.","APAGA LOS REPETIDORES."},
 {"ESTEFI: ERA EL ESTOMAGO!","DANIEL: FALTA EL JEFE.","CHUCHO: ES UN MEGAFONO.","HAZ QUE OIGAN SU VERSION."},
 {"DANIEL: MI MAMA ES CHILENA.","CHUCHO: TU SABES LLEGAR.","ESTEFI: ESO VIENE CON MAPA?","SIGUE LAS PISTAS DIBUJADAS."},
 {"DANIEL: CASI LO DESCIFRO.","ESTEFI: LEE EL OTRO LADO.","CHUCHO: PRIMERO EL CASTILLO.","ENCUENTRA EL ESCENARIO."},
 {"NADIA: SOLO UNA COSITA.","ALI: OFERTA EN OTRO PASILLO!","ESTEFI: Y LA CAJA ABIERTA?","SIGUE LA LISTA DE UTILERIA."},
 {"DANIEL: LE PONGO UN APODO.","CHUCHO: AHORA SE VOLVIO ESO!","ALI: NO LO LLAMEN TANQUE.","APRENDE EL NOMBRE Y ESQUIVA."},
 {"CHUCHO: YA TENEMOS IDEAS.","ESTEFI: QUIEN DIO GRABAR?","DANIEL: DESDE EL PRINCIPIO.","TERMINA NUESTRA ULTIMA TOMA."}
};
const char* const rewrite[5][3]={
 {"ESTEFI: MAS PROTECCIONES!","DANIEL: PUSE COLCHONETAS.","CHUCHO: AHORA TOCA SALTAR."},
 {"ESTEFI: NO DIJE ESO.","DANIEL: OTRO REPETIDOR!","CHUCHO: YA TIENE SECUELA."},
 {"DANIEL: POR AQUI ES.","ESTEFI: SEGUN QUE PISTA?","CHUCHO: MIRA LOS DIBUJOS."},
 {"NADIA: ABRIERON OTRA CAJA.","ALI: AL FONDO A LA DERECHA.","ESTEFI: ESO DIJISTE ANTES!"},
 {"CHUCHO: ESE TIENE ALAS.","DANIEL: LO LLAME PAJARITO.","ESTEFI: PONLE ALGO FACIL!"}
};
const char* const outros[5][4]={
 {"NADIA: POR FIN LLEGARON!","ALI: NOSOTROS POR ESCALERA.","ESTEFI: TE LO DIJIMOS.","CHUCHO: VIERON LA VISTA?"},
 {"ESTEFI: ERA EL ESTOMAGO.","SISTEMA: OPERACION EXITOSA!","ESTEFI: OTRA VEZ CON ESO?","DANIEL: EL TITULO QUEDO."},
 {"ESTEFI: VOLTEA LA TARJETA.","DANIEL: AQUI ESTA EL MAPA.","CHUCHO: NO ERA HEREDITARIO.","ALI: LES VENDO OTRO?"},
 {"NADIA: COMPRAMOS DE TODO.","CHUCHO: SOLO ERA UNA PILA.","ALI: LA PILA VA APARTE.","ESTEFI: QUE GRAN PRODUCCION."},
 {"DANIEL: YA NO PONGO APODOS.","CHUCHO: NI UNO CHIQUITO?","ESTEFI: NO DIGAS DRAGON.","ALI: YA LO DIJERON."}
};
const u8 colors[5][4]={{0x0f,0x07,0x17,0x27},{0x0f,0x05,0x15,0x35},{0x0f,0x07,0x17,0x27},{0x0f,0x06,0x16,0x36},{0x0f,0x04,0x14,0x34}};
/* 32 symbols: omit the ambiguous pairs 0/O and 1/I. */
const u8 backdrop[5][3]={{0x01,0x11,0x21},{0x00,0x10,0x20},{0x09,0x19,0x29},{0x01,0x11,0x21},{0x02,0x12,0x22}};
const char code_alphabet[]="23456789ABCDEFGHJKLMNPQRSTUVWXYZ";
const char* const root_options[5]={"CONTINUAR AVENTURA","NUEVA AVENTURA","CARGAR CONTRASENA","JUEGOS DEL ESTUDIO","COMO JUGAR"};
const char* const pause_options[6]={"CONTINUAR","REINTENTAR DESDE CLAQUETA","VOLVER AL ESTUDIO","CAMBIAR DIFICULTAD","VER CONTRASENA","VER CONTROLES"};
const char* const clue_lines[9]={"ALUMBRA SIN USAR UNA PILA.","CAE Y NO SE LASTIMA.","TIENE HOJAS Y NO ES LIBRO.","SALE CUANDO ACABA LA NOCHE.","ES PEQUENA, MOJA BASTANTE.","CRECE SIN SUBIR ESCALERAS.","NO LO MIRES DE FRENTE.","LLENA UN VASO CON AMIGAS.","TIENE RAICES, NO PELO."};
const char* const clue_options[3]={"SOL","GOTA","ARBOL"};
static void service(u8 op,u8 arg){adv_service_op=op;adv_service_arg=arg;adv_service();}
static void address(u16 a){PPUADDR=a>>8;PPUADDR=(u8)a;}
static void put(u8 x,u8 y,const char* s){address(0x2000+((u16)y<<5)+x);while(*s)PPUDATA=*s++;}
static void center(u8 y,const char* s){u8 n=0;while(s[n])++n;put((32-n)/2,y,s);}
static void off(void){R(0x2000)=0;R(0x2001)=0;adv_sprite_tail=0;R(0x5101)=1;ready=0;hud_on=0;menu_dirty=0;help_dirty=0;ex_on=0;R(0x5104)=2;hide();}
static void on(void){R(0x2005)=0;R(0x2005)=0;R(0x2000)=0x88;R(0x2001)=0x1e;}
static void palette(u8 world){u8 i;
 address(0x3f00);
 PPUDATA=0x0f;PPUDATA=0x07;PPUDATA=0x27;PPUDATA=0x30;
 for(i=0;i<4;++i)PPUDATA=colors[world][i];
 PPUDATA=0x0f;for(i=0;i<3;++i)PPUDATA=backdrop[world][i];
 PPUDATA=0x0f;PPUDATA=0x09;PPUDATA=0x19;PPUDATA=0x29;
 for(i=0;i<3;++i){PPUDATA=0x0f;PPUDATA=0x0f;PPUDATA=0x37;PPUDATA=i==0?0x2b:(i==1?0x21:0x30);}
 PPUDATA=0x0f;PPUDATA=0x0f;PPUDATA=0x16;PPUDATA=0x30;
}
extern u8 plaza_attrs[64];
static void tint(u8 tx,u8 ty,u8 pal);
static void clear(void){u16 i;off();art_bank=60;sprite_bank=59*4;R(0x5123)=60;palette(0);address(0x2000);
 for(i=0;i<960;++i)PPUDATA=32;
 for(i=0;i<64;++i){PPUDATA=0;plaza_attrs[i]=0;}
 address(0x3f04);PPUDATA=0x0f;PPUDATA=0x0f;PPUDATA=0x17;PPUDATA=0x37;
 address(0x2042);for(i=0;i<28;++i)PPUDATA=238;
 address(0x2362);for(i=0;i<28;++i)PPUDATA=238;
}
static void portrait(u8 who,u8 x,u8 y){u8 row,j;
 for(row=0;row<4;++row){address(0x2000+((u16)(y+row)<<5)+x);for(j=0;j<4;++j)PPUDATA=128+who*16+row*4+j;}
 for(row=0;row<4;++row)for(j=0;j<4;++j)tint(x+j,y+row,1);
 address(0x23c0);for(j=0;j<64;++j)PPUDATA=plaza_attrs[j];
}
static void title(const char* s){center(4,s);}
static void card(const char* heading,const char* const* lines,u8 n){u8 i;clear();title(heading);portrait(host,14,6);
 for(i=0;i<n;++i)center(12+i*2,lines[i]);
 center(24,"A / START: SEGUIR");center(26,adv_ui_page==UI_REWRITE?"B: OMITIR":"B: VOLVER AL ESTUDIO");on();
}
static void cursor(u8 x,u8 y){spr=0;R(0x200)=y;R(0x201)=162;R(0x202)=3;R(0x203)=x;}
static void poll(void){wait_frame();oldpad=pad;pad=pad_read();pressed=pad&~oldpad;if(!paused)service(0,0);}
static u8 countbits(u16 n){u8 count=0;while(n){count+=n&1;n>>=1;}return count;}
static void byte(u8 x,u8 y,u8 n){address(0x2000+((u16)y<<5)+x);PPUDATA='0'+n/10;PPUDATA='0'+n%10;}
static u8 open_stage(u8 s){
 if(s<2)return s==0||(adv_save.cleared&1);
 if(s<4)return (adv_save.cleared&3)==3&&(s==2||(adv_save.cleared&4));
 if(s<6)return (adv_save.cleared&15)==15&&(s==4||(adv_save.cleared&16));
 return (adv_save.cleared&63)==63&&(s!=8||adv_save.tasks==7);
}
extern u8 plaza_attrs[64];
static void tint(u8 tx,u8 ty,u8 pal){u8 a,shift;a=(ty/4)*8+tx/4;shift=((ty/2)&1)*4+((tx/2)&1)*2;plaza_attrs[a]=(plaza_attrs[a]&~(3<<shift))|(pal<<shift);}
static void room(void){u8 x,y,i,tile,world=adv.world;Platform* p;
 off();art_bank=54+world;sprite_bank=59*4;R(0x5123)=art_bank;palette(world);
 address(0x2000);
 for(y=0;y<30;++y)for(x=0;x<32;++x){
  tile=32;
  if(y>=7&&y<26){
   if(y>=19&&y<23)tile=136+(y-19)*4+(x&3);
   else if(y>=9&&y<11&&(x+adv.room*3)%13<4)tile=152+(y-9)*4+(x+adv.room*3)%13;
   else if((y>=22||((world==1||world==3||world==4)&&y>=11))&&(x+adv.room)%8<2)tile=160+((y+2)&3)*2+(x+adv.room)%8;
   else if((x*7+y*3+adv.room)%73==0)tile=168;
  }
  PPUDATA=tile;
 }
 for(i=0;i<64;++i)plaza_attrs[i]=i>=8&&i<56?0xaa:0;
 for(i=0;i<5;++i){p=&adv.platforms[i];if(!p->w||p->kind==1)continue;
  for(y=0;y<2;++y){address(0x2000+((u16)(p->y/8+y)<<5)+p->x/8);for(x=0;x<p->w/8;++x)PPUDATA=128+(x&3)+y*4;}
  for(x=0;x<p->w/8;++x)tint(p->x/8+x,p->y/8,1);
  if(p->kind==2){address(0x2000+((u16)(p->y/8)<<5)+p->x/8+1);PPUDATA=206;PPUDATA=207;}
 }
 for(y=0;y<4;++y){address(0x2000+((u16)(adv.exit_y/8-1+y)<<5)+28);PPUDATA=192+y*2;PPUDATA=193+y*2;}
 for(y=0;y<4;++y)tint(28,adv.exit_y/8-1+y,1);
 address(0x23c0);for(i=0;i<64;++i)PPUDATA=plaza_attrs[i];
 put(2,28,"START:PAUSA");put(18,28,"ARRIBA:SALIR");
 hud_on=1;on();
}
static void menu(u8 page,u8 selected){u8 i,s;clear();
 if(page==UI_ROOT){
  for(s=0;s<2;++s){address(0x2000+(3+s)*32+5);for(i=0;i<22;++i)PPUDATA=192+s*22+i;}
  center(6,"UNA ULTIMA TOMA");
  for(i=0;i<3;++i)portrait(i,5+i*9,8);
  for(i=0;i<5;++i)center(14+i*2,root_options[i]);
  center(25,"A: ELEGIR   CRUCETA: MOVER");
 }else if(page==UI_STUDIO){
  title("LA MESA DE IDEAS");center(6,anames[host]);
  put(3,8,"TOMAS");byte(9,8,countbits(adv_save.cleared));put(15,8,"CINTAS");byte(22,8,countbits(adv_save.tapes));
  for(i=0;i<6;++i){
   s=i<3?i*2:i+3;
   put(4,11+i*2,world_names[i]);
   if(!open_stage(s))put(2,11+i*2,"-");else if(adv_save.cleared&((u16)1<<s))put(2,11+i*2,"+");
  }
  if(!open_stage(selected<3?selected*2+adv_trial:selected+3))center(24,"TERMINA LA IDEA ANTERIOR");
  else if(selected<3){center(24,adv_trial?"< > TOMA 2     A: ENSAYAR":"< > TOMA 1     A: ENSAYAR");}
  else center(24,"A: ENSAYAR   B: MENU");
  center(26,"SELECT: ACTOR  START: CODIGO");
 }else{
  title("PAUSA / OTRA TOMA");center(7,level_names[adv.stage]);
  for(i=0;i<6;++i)center(11+i*2,pause_options[i]);
  center(24,adv_save.easy?"MODO: ENSAYO TRANQUILO":"MODO: TOMA NORMAL");
  center(26,"START: CONTINUAR");
 }
 on();
}
static void menu_loop(u8 page){u8 selected,count,changed;
 selected=page==UI_PAUSE?0:adv_ui_sel;count=page==UI_ROOT?5:6;if(selected>=count)selected=0;
 menu(page,selected);
 for(;;){
  cursor(page==UI_STUDIO?8:16,(page==UI_ROOT?112:88)+selected*16);poll();changed=0;
  if(pressed&UP){selected=selected?selected-1:count-1;changed=1;}
  if(pressed&DOWN){selected=(selected+1)%count;changed=1;}
  if(page==UI_STUDIO){
   if(changed){adv_trial=selected<3&&(adv_save.cleared&((u16)1<<(selected*2)))?1:0;}
   if(pressed&(LEFT|RIGHT)){adv_trial^=1;changed=1;}
   if(pressed&SELECT){host=(host+1)%3;changed=1;}
   if(pressed&START){adv_ui_sel=selected;adv_command=2;return;}
  }
  if(pressed&B){adv_command=page==UI_PAUSE?1:0;if(page!=UI_ROOT)return;}
  if(page==UI_PAUSE&&(pressed&START)){adv_command=1;return;}
  if(pressed&A){
   if(page==UI_STUDIO){adv_ui_sel=selected;adv_command=1;return;}
   if(page==UI_ROOT&&selected==0&&!adv_save.valid){service(2,2);continue;}
   adv_command=selected+1;if(page==UI_ROOT)adv_ui_sel=selected;return;
  }
  if(changed){if(!paused)service(2,4);menu(page,selected);}
 }
}
static void help(void){clear();title("COMO JUGAR");
 center(8,"CRUCETA: MOVERSE");center(11,"A: SALTA / MANTEN MAS ALTO");center(14,"B: ACCION DEL PERSONAJE");
 center(17,"ARRIBA: CLAQUETA O PUERTA");center(20,"START: PAUSA Y AYUDA");
 center(23,host==0?"CHUCHO: GOLPE Y REBOTE":(host==1?"ESTEFI: DISPARO A DISTANCIA":"DANIEL: DESVIA PROYECTILES"));center(25,"A / B: VOLVER");on();
 for(;;){poll();if(pressed&(A|B|START)){adv_command=0;return;}}
}
/* Version 1: 44 payload bits + CRC16 = twelve five-bit symbols. */
static void setbits(u8* data,u8 at,u8 n,u16 value){u8 i;for(i=0;i<n;++i){if(value&1)data[at>>3]|=1<<(at&7);value>>=1;++at;}}
static u16 getbits(const u8* data,u8 at,u8 n){u8 i;u16 result=0,mask=1;for(i=0;i<n;++i){if(data[at>>3]&(1<<(at&7)))result|=mask;mask<<=1;++at;}return result;}
static u16 crc(const u8* data){u8 i,j,v;u16 sum=0xffff;
 for(i=0;i<6;++i){v=data[i];if(i==5)v&=15;sum^=(u16)v<<8;for(j=0;j<8;++j)sum=(sum&0x8000)?(sum<<1)^0x1021:sum<<1;}
 return sum;
}
static void encode(void){u8 data[8],i;for(i=0;i<8;++i)data[i]=0;
 setbits(data,0,4,1);setbits(data,4,9,adv_save.cleared);setbits(data,13,9,adv_save.perfect);
 setbits(data,22,8,adv_save.tapes);setbits(data,30,3,adv_save.tasks);setbits(data,33,1,adv_save.easy);
 setbits(data,44,16,crc(data));for(i=0;i<12;++i)adv_code[i]=(u8)getbits(data,i*5,5);
}
static u8 decode(void){u8 data[8],i,tapes,tasks;u16 cleared,perfect;
 for(i=0;i<8;++i)data[i]=0;for(i=0;i<12;++i)setbits(data,i*5,5,adv_code[i]);
 if(getbits(data,0,4)!=1||getbits(data,34,10)||getbits(data,44,16)!=crc(data))return 0;
 cleared=getbits(data,4,9);perfect=getbits(data,13,9);tapes=getbits(data,22,8);tasks=(u8)getbits(data,30,3);
 if(perfect&~cleared)return 0;
 for(i=1;i<6;++i)if((cleared&((u16)1<<i))&&!(cleared&((u16)1<<(i-1))))return 0;
 if((cleared&0x1c0)&&(cleared&63)!=63)return 0;
 if((cleared&0x100)&&tasks!=7)return 0;
 if((cleared&3)&&!(tasks&1))return 0;
 if((cleared&12)&&!(tasks&2))return 0;
 if((cleared&48)&&!(tasks&4))return 0;
 if((tasks&2)&&(cleared&3)!=3)return 0;
 if((tasks&4)&&(cleared&15)!=15)return 0;
 for(i=1;i<6;i+=2)if((tapes&(1<<i))&&!(cleared&((u16)1<<(i-1))))return 0;
 if((tapes&0xc0)&&(cleared&63)!=63)return 0;
 if((tapes&0x30)&&(cleared&15)!=15)return 0;
 if((tapes&0x0c)&&(cleared&3)!=3)return 0;
 adv_save.valid=1;adv_save.cleared=cleared;adv_save.perfect=perfect;adv_save.tapes=tapes;adv_save.tasks=tasks;adv_save.easy=(u8)getbits(data,33,1);return 1;
}
static void code_draw(u8 selected){u8 i;clear();title(adv_password_load?"CARGAR CONTRASENA":"TU CONTRASENA");
 center(9,"GUARDA ESTE CODIGO");
 for(i=0;i<12;++i){address(0x2000+14*32+5+i+i/4);PPUDATA=code_alphabet[adv_code[i]];}
 if(adv_password_load){
  address(0x2000+16*32+5+selected+selected/4);PPUDATA='+';
  center(19,adv_code_error?"CODIGO INCORRECTO. REVISA.":"< > POSICION  ARRIBA/ABAJO");
  center(22,"A: CARGAR   B: CANCELAR");
 }else{center(19,"REANUDA DESDE EL ESTUDIO");center(22,"A / B: VOLVER");}
 center(25,"NO GUARDA LA SALA ACTUAL");on();
}
static void password(void){u8 selected=0,changed,repeat=0;
 if(!adv_password_load)encode();code_draw(selected);
 for(;;){poll();changed=0;
  if(pad&(UP|DOWN|LEFT|RIGHT)){if(pad!=oldpad)repeat=0;else if(++repeat>=24){pressed|=pad&(UP|DOWN|LEFT|RIGHT);repeat=20;}}else repeat=0;
  if(pressed&B){adv_command=0;return;}
  if(pressed&A){
   if(!adv_password_load){adv_command=0;return;}
   if(decode()){adv_command=1;return;}adv_code_error=1;code_draw(selected);
  }
  if(adv_password_load){
   if(pressed&LEFT){selected=selected?selected-1:11;changed=1;}
   if(pressed&RIGHT){selected=(selected+1)%12;changed=1;}
   if(pressed&UP){adv_code[selected]=(adv_code[selected]+1)&31;changed=1;}
   if(pressed&DOWN){adv_code[selected]=(adv_code[selected]-1)&31;changed=1;}
   if(changed){adv_code_error=0;code_draw(selected);}
  }
 }
}
static void clue(void){u8 selected=0,i;clear();title("LA PISTA DEL CAMINO");
 center(9,clue_lines[adv.clue]);center(12,"QUE SENAL DEBES SEGUIR?");
 for(i=0;i<3;++i)center(16+i*2,clue_options[i]);center(25,"A: ELEGIR   B: VOLVER");on();
 for(;;){cursor(64,128+selected*16);poll();
  if(pressed&UP)selected=selected?selected-1:2;if(pressed&DOWN)selected=(selected+1)%3;
  if(pressed&B){adv_command=0;return;}
  if(pressed&A){if(selected==adv.clue%3){adv_command=1;return;}service(2,2);}
 }
}
void adv_ui(void){u8 i,w=adv.stage<6?adv.stage/2:(adv.stage==6?3:4);
 if(adv_ui_page==UI_ROOM){room();return;}
 adv_command=0;
 if(adv_ui_page==UI_ROOT||adv_ui_page==UI_STUDIO||adv_ui_page==UI_PAUSE){menu_loop(adv_ui_page);return;}
 if(adv_ui_page==UI_PASSWORD){password();return;}
 if(adv_ui_page==UI_HELP){help();return;}
 if(adv_ui_page==UI_CLUE){clue();return;}
 if(adv_ui_page==UI_INTRO)card(level_names[adv.stage],intro[adv.stage],4);
 else if(adv_ui_page==UI_REWRITE)card("Y SI CAMBIAMOS ESTO?",rewrite[adv.world],3);
 else if(adv_ui_page==UI_OUTRO)card("VOLVEMOS AL ESTUDIO",outros[w],4);
 else{
  clear();
  if(adv_ui_page==UI_TASK){
   title("PREPARAMOS EL SKETCH");portrait(adv.stage/2,14,6);
   center(12,adv.stage<2?"CHUCHO PREPARA EL DECORADO":(adv.stage<4?"ESTEFI ENSAYA SU ENTRADA":"BUSCAMOS A DANIEL"));
   center(15,adv.stage<2?"RESUELVE DOS REPARACIONES":(adv.stage<4?"COMPLETA DOCE NOTAS":"ENCUENTRALO UNA VEZ"));
   center(19,"A: ENSAYAR   B: ESTUDIO");
   if(adv_task_fails>=2)center(23,"SELECT: EL EQUIPO TE AYUDA");
   else center(23,"TRAS DOS FALLOS HAY AYUDA");
  }else if(adv_ui_page==UI_FAILURE){
   title("OTRA TOMA!");portrait(host,14,7);center(14,"VUELVE A LA ULTIMA CLAQUETA");
   center(18,"A: REINTENTAR B: ESTUDIO");if(adv.death_count>=2)center(22,"SELECT: ENSAYO TRANQUILO");
  }else if(adv_ui_page==UI_RESULT){
   title("TOMA COMPLETA!");portrait(host,14,7);center(14,level_names[adv.stage]);
   center(18,adv_save.perfect&((u16)1<<adv.stage)?"MEDALLA: SIN UN RASGUNO":"LA IDEA YA ESTA PROBADA");
   center(22,"A: VOLVER A LA REUNION");
  }else if(adv_ui_page==UI_CONFIRM){
   title("EMPEZAR DE NUEVO?");center(12,"SE BORRA LA SESION ACTUAL");center(16,"CONSERVA TU CONTRASENA");
   center(22,"A: NUEVA   B: CANCELAR");
  }else if(adv_ui_page==UI_PROLOGUE){
   title("EL SKETCH DEL VIDEOJUEGO");for(i=0;i<3;++i)portrait(i,5+i*9,7);
   center(13,"CHUCHO: Y SI SOMOS EL JUEGO?");center(16,"ESTEFI: TENGO VARIAS IDEAS.");
   center(19,"DANIEL: HAY QUE PROBARLAS.");center(22,"IMAGINA, ENSAYA Y GRABA.");center(25,"A: VAMOS A LA MESA DE IDEAS");
  }else if(adv_ui_page==UI_ENDING){
   title("EL SKETCH ERA ESTA REUNION");for(i=0;i<3;++i)portrait(i,5+i*9,7);
   center(13,"NADIA: LO GRABARON TODO.");center(16,"ALI: INCLUSO LOS INTENTOS.");
   center(19,adv_save.tapes==255?"BONUS: GUARDA LOS BLOOPERS!":"LOS TRES: OTRA TOMA?");center(22,"GRACIAS POR JUGAR!");center(25,"A: ESTUDIO Y TOMAS EXTRA");
  }
  on();
 }
 for(;;){poll();
  if(pressed&B){adv_command=0;return;}
  if(pressed&(A|START)){adv_command=1;return;}
  if((pressed&SELECT)&&((adv_ui_page==UI_TASK&&adv_task_fails>=2)||(adv_ui_page==UI_FAILURE&&adv.death_count>=2))){adv_command=2;return;}
 }
}
