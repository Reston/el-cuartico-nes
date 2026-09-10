#pragma code-name(push, "EXTRACODE")
/* Shared broadcast slate. All text fits inside the 28-column safe area. */
const u8 ui_palette[16]={0x0f,0x07,0x27,0x30, 0x0f,0x09,0x19,0x29, 0x0f,0x06,0x16,0x26, 0x0f,0x07,0x17,0x27};
const char* const help_lines[3][5]={
 {"COMPLETA 12 REPARACIONES","CRUCETA: MOVERSE","A: ABRIR UNA REPARACION","B: CORRER CUANDO ESTE LISTO","EL RELOJ PARA EN LOS PANELES"},
 {"CONSIGUE 20 ACIERTOS","LEE A, B O LA DIRECCION","PULSA DENTRO DEL RECUADRO","PRIMERO PRACTICA CON A","PUEDES FALLAR CUATRO VECES"},
 {"ENCUENTRA A DANIEL 3 VECES","CRUCETA: MOVER EL CURSOR","B: LUPA   A: ELEGIR","UN ERROR CUESTA 5 SEGUNDOS","CRUZA BORDES CON FLECHAS"}
};
const char* const panel_names[4]={"CABLES","ENFOQUE","MEZCLADORA","MEMORIA"};
const char* const panel_help[4][3]={
 {"UNE LOS NUMEROS IGUALES","ARRIBA/ABAJO: ELEGIR","A: CONECTAR"},
 {"ALINEA ESTRELLA Y RECUADRO","IZQUIERDA/DERECHA: MOVER","A: CONFIRMAR"},
 {"ESPERA LA SENAL EN EL MARCO","LA ESTRELLA SE MUEVE SOLA","A: ATRAPAR"},
 {"MIRA LAS CUATRO DIRECCIONES","REPITELAS CON LA CRUCETA","ESPERA LA SECUENCIA COMPLETA"}
};

void ui_count(u8 x,u8 y,u8 value){
 if(value>99)value=99;addr(0x2000+((u16)y<<5)+x);PPUDATA='0'+value/10;PPUDATA='0'+value%10;
}
void episode_progress(u8 y){
 center(y,remix?"REMIX 1     0/3 SELLOS":"EPISODIO 1  0/3 SELLOS");
 addr(0x2000+((u16)y<<5)+(remix?11:14));PPUDATA='1'+episode;
 addr(0x2000+((u16)y<<5)+17);
 PPUDATA='0'+(completed&1)+((completed>>1)&1)+((completed>>2)&1);
}
void slate(void){off();chr_bank(49);load_palette(palette,32);load_palette(ui_palette,16);load_resource(4);}
void ui_heading(const char* text,u8 color){u8 i;center(10,text);addr(0x23d1);for(i=0;i<6;++i)PPUDATA=color*80;}
void help_screen(void){u8 i;
 slate();ui_heading("COMO JUGAR",0);
 if(paused&&host==0&&task_active){
  center(12,panel_names[repair_task]);
  for(i=0;i<3;++i)center(14+i*2,panel_help[repair_task][i]);
  center(20,"B: CERRAR EL PANEL");center(22,"TIEMPO SIN LIMITE");
 }else{
  center(12,game_title());for(i=0;i<5;++i)center(14+i*2,episode?live_help[host][i]:help_lines[host][i]);
 }
 center(26,paused?"SELECT / B: VOLVER A PAUSA":"< > CAMBIAR PERSONAJE");
 center(28,paused?"START: CONTINUAR":((completed&masks[host])?"SELLO LISTO   B: MENU":"A:JUEGA B:MENU"));on();
}
void menu_help(void){mode=HELP;help_screen();}
void pause_screen(void){
 slate();ui_heading("PAUSA",3);center(12,game_title());
 print(6,16,"START");print(13,16,"CONTINUAR");print(6,18,"A");print(13,18,"REINTENTAR");print(6,20,"B");print(13,20,"VOLVER AL MENU");
 center(22,"TIEMPO Y MUSICA EN PAUSA");center(26,"SELECT: VER CONTROLES");center(28,"CONTINUA CUANDO QUIERAS");on();
}
void pause_open(void){
 pause_art=art_bank;pause_sprite=sprite_bank;pause_hud=hud_on;paused=1;pause_help=0;
 silence();off();pause_capture();pause_screen();
}
void pause_close(void){
 off();pause_restore();chr_bank(pause_art);sprite_bank=pause_sprite;
 paused=0;pause_help=0;music_restore=1;if(mode==RHYTHM&&hold_slot<3)hold_resume=1;hud_update();hud_on=pause_hud;on();
}
void result_screen(void){u8 n,total;u16 errors;
 slate();ui_heading(last_win?(result_grade==3?"TOMA PERFECTA!":"SELLO CONSEGUIDO!"):"OTRA TOMA",last_win?1:2);center(12,names[host]);
 if(!last_win)center(14,host==1?"CINCO FALLOS EN LA TOMA":(host==0&&health==0?"SIN CORAZONES":"SE ACABO EL TIEMPO"));
 print(5,16,"PUNTOS");number(20,16,attempt_score);
 n=host==0?repairs:(host==1?hits:found);total=host==0?12:(host==1?rhythm_goal():3);
 if(episode&&host==2){print(5,18,"DANY 3/3  OBJETOS 0/6");addr(0x2000+18*32+10);PPUDATA='0'+found;addr(0x2000+18*32+23);PPUDATA='0'+collected_props;}
 else{print(5,18,host==0?"REPARACIONES":(host==1?"ACIERTOS":"ENCUENTROS"));ui_count(20,18,n);print(22,18,"/");ui_count(23,18,total);}
 errors=(u16)misses+task_mistakes;print(5,20,"ERRORES");if(errors>99)print(22,20,"99+");else ui_count(23,20,(u8)errors);
 episode_progress(22);center(26,last_win?"A / START: CONTINUAR":"A / START: REINTENTAR");center(28,"B: VOLVER AL MENU");
 mode=RESULT;music_start(last_win?4:5);on();
}

#pragma code-name(pop)
