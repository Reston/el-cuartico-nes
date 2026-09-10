/* Episode two: linked broadcast systems, held notes and optional location clues. */
#pragma code-name(push, "EXTRACODE")
const char* const live_titles[3]={"SALVEMOS EL DIRECTO","EL GRAN NUMERO","DANY LLEGA TARDE"};
const char* const live_goals[3]={"3 ENLACES AL AIRE","49 ACIERTOS CON SOSTENIDAS","3 ENCUENTROS + OBJETOS"};
const char* const live_help[3][5]={
 {"ENERGIA ANTES DE REPARAR","LUEGO CAMARA Y MEZCLADORA","ELIGE QUE REPARAR PRIMERO","MEMORIA CIERRA CADA ENLACE","COMPLETA TRES ENLACES"},
 {"PULSA LA NOTA AL LLEGAR","AL MARCO DE LA IZQUIERDA","SI TIENE COLA: MANTEN","BARRA VACIA: SUELTA","49 ACIERTOS / 4 FALLOS"},
 {"ENCUENTRA A DANIEL 3 VECES","MICRO Y GUION: OPCIONALES","ACERCATE Y PULSA A","PISTAS, PUNTOS Y TIEMPO","B: LUPA   CRUCETA: MOVER"}
};
const char* const link_names[3]={"ENLACE 1: ABRIMOS EL PROGRAMA","ENLACE 2: INVITADO EN LINEA","ENLACE 3: SALIMOS AL AIRE"};
const char* game_title(void){return episode?live_titles[host]:titles[host];}
const char* game_goal(void){return episode?live_goals[host]:goals[host];}
u8 rhythm_goal(void){return episode?49:20;}
void mission_screen(void){u8 i;
 slate();ui_heading("EPISODIO 2: EN DIRECTO",3);center(12,live_titles[host]);
 for(i=0;i<5;++i)center(14+i*2,live_help[host][i]);
 center(25,"A / START: COMENZAR");center(27,"B: VOLVER AL MENU");
 mode=MISSION;paused=0;music_start(0);on();
}
void campaign_next(u8 fresh){u8 i;
 if(fresh||episode){episode=0;remix=!fresh;score=0;for(i=0;i<3;++i)first_medals[i]=0;}
 else{episode=1;for(i=0;i<3;++i)first_medals[i]=medals[i];}
 completed=0;for(i=0;i<3;++i)medals[i]=0;host=0;hub();
}
void linked_start(void){u8 i;link_mask=0;seconds=99;for(i=0;i<4;++i)alarm[i]=0;alarm[0]=22;}
void linked_success(u8 station){
 link_mask|=1<<station;cheer=45;
 if(station==0){alarm[1]=alarm[2]=22;}
 if(link_mask==7)alarm[3]=22;
 if(link_mask==15){
  if(repairs==12){attempt_score+=seconds*10;finish(1);return;}
  link_mask=0;alarm[0]=22;seconds=seconds<91?seconds+8:99;
 }
}
void linked_second(void){u8 i;
 hud_dirty=1;
 for(i=0;i<4;++i)if(alarm[i]&&!--alarm[i]){
  alarm[i]=18;if(health)--health;if(misses<255)++misses;combo=1;react(1);sound(2);
 }
 if(seconds)--seconds;if(!health||!seconds)finish(0);
}
const char* linked_status(void){
 if(task_active)return "EL RELOJ ESPERA EN EL PANEL";
 if(!(link_mask&1))return "ENERGIA: REPARA LOS CABLES";
 if(link_mask==7)return "TODO LISTO: REINICIA LA SENAL";
 if(studio_station<4)return station_prompts[studio_station];
 return "CAMARA Y MEZCLA: ELIGE EL ORDEN";
}
void linked_draw(void){u8 i;
 for(i=0;i<4;++i)if(!alarm[i])sprite(sx[i]-4,sy[i]-30,(link_mask&(1<<i))?39:CROSS,3);
}
void props_start(void){u8 i;
 prop_mask=0;clue_timer=0;
 for(i=0;i<2;++i){prop_area[i]=(target_district+i+1)%district_count;prop_x[i]=32+i*144+(random()&3)*8;}
}
u8 prop_cursor(void){u8 i;
 /* The focused face always owns A, including inside the magnifier. */
 if(hover_npc<24||cursor_y<72||cursor_y>88)return 255;
 for(i=0;i<2;++i)if(!(prop_mask&(1<<i))&&district==prop_area[i]&&cursor_x+8>=prop_x[i]&&cursor_x<=prop_x[i]+8)return i;
 return 255;
}
u8 prop_collect(void){u8 i=prop_cursor();
 if(i==255)return 0;
 prop_mask|=1<<i;++collected_props;attempt_score+=150;
 seconds=seconds<89?seconds+10:99;clue_timer=240;reaction_time=0;hud_dirty=1;sound(1);return 1;
}
void props_draw(void){u8 i,j,p=prop_cursor();
 for(i=0;i<2;++i)if(!(prop_mask&(1<<i))&&district==prop_area[i]){
  for(j=0;j<4;++j)sprite(prop_x[i]+(j&1)*8,72+(j>>1)*8,72+i*4+j,1);
  if(p==i)focus(prop_x[i]-2,70,3);
 }
}
#pragma code-name(pop)
