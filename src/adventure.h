#ifndef ADVENTURE_H
#define ADVENTURE_H
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u16;
typedef signed int s16;
#define R(a) (*(volatile u8*)(a))
#define PPUADDR R(0x2006)
#define PPUDATA R(0x2007)
#define A 128
#define B 64
#define SELECT 32
#define START 16
#define UP 8
#define DOWN 4
#define LEFT 2
#define RIGHT 1
#define UI_ROOT 0
#define UI_STUDIO 1
#define UI_INTRO 2
#define UI_PAUSE 3
#define UI_RESULT 4
#define UI_PASSWORD 5
#define UI_HELP 6
#define UI_TASK 7
#define UI_CONFIRM 8
#define UI_ENDING 9
#define UI_CLUE 10
#define UI_ROOM 20
#define UI_REWRITE 21
#define UI_FAILURE 22
#define UI_OUTRO 23
#define UI_PROLOGUE 24
#define UI_RELAY 25
#define UI_BOOK 11
#define UI_ROUTES 12
#define UI_NPC 13
#define MAX_ROOMS 16
#define ECOUNT 3
#define BCOUNT 3
typedef struct {u8 x,y,w,kind;} Platform;
typedef struct {u8 x,y,lo,hi,type,hp,tick,inv; s8 dir;} Enemy;
typedef struct {u8 x,y,life,owner; s8 vx,vy;} Bullet;
typedef struct {
 u8 valid,easy,tasks,tapes;
 u16 cleared,perfect;
} AdvSave;
typedef struct {
 u8 stage,room,world,health,x,facing,ground,coyote,buffer,attack,cooldown,inv,tick;
 s16 y,vy;
 u8 checkpoint,damaged,keys,tape,exit_y,gate_x,gate_y,tape_x,tape_y,dead,hitstop;
 u8 boss_hp,boss_tick,boss_inv,room_seen,helped,flash,clue,death_count;
 u8 flags[MAX_ROOMS];
 Platform platforms[5];
 Enemy enemies[ECOUNT];
 Bullet bullets[BCOUNT];
 u8 boss_x,boss_y,props,hud_state;
 u8 run_phase,landing,hurt;
 u8 boss_round,boss_marks,bridge_width;
} AdvState;
extern u8 adv_sprite_tail,adv_sprite_actor;
extern AdvState adv;
extern AdvSave adv_save;
extern u8 adv_bank,adv_service_op,adv_service_arg,adv_ui_page,adv_command,adv_ui_sel;
extern u8 adv_trial,adv_code[12],adv_code_error,adv_activity_result,adv_task_fails,adv_password_load;
extern u8 mode,paused,pad,oldpad,pressed,host,spr;
extern volatile u8 ready,frame,art_bank,sprite_bank,hud_on,ex_on,menu_dirty,help_dirty;
extern u8 hud[32],status_row[32];
extern void wait_frame(void);
extern u8 pad_read(void);
extern void hide(void);
extern void __fastcall__ adv_shape(u8 x,u8 y,u8 tile,u8 w,u8 h,u8 attr);
extern void __fastcall__ sprite(u8 x,u8 y,u8 tile,u8 attr);
extern void adv_present(void);
extern void adv_service(void);
#endif
