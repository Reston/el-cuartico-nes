.export _wait_frame, _pad_read, _main_entry
.export __STARTUP__ : absolute = 1
.export _frame, _ready, _hud, _hud_on, _art_bank, _sprite_bank, _ex_on, _title_extended
.export _menu_dirty, _menu_rows
.import _main, _spr, zerobss, copydata, incsp3
.importzp c_sp, ptr1
.segment "HEADER"
.byte "NES",$1A,8,32,$50,0,0,0,0,0,0,0,0,0
.segment "BSS"
_frame: .res 1
_ready: .res 1
_hud_on: .res 1
_art_bank: .res 1
_sprite_bank: .res 1
_hud: .res 32
_ex_on: .res 1
_menu_dirty: .res 1
_menu_rows: .res 96
.segment "STARTUP"
_main_entry:
 sei
 cld
 ldx #$40
 stx $4017
 ldx #$ff
 txs
 inx
 stx $2000
 stx $2001
 stx $4010
 ; MMC5: reset stub/vectors stay in the last 8 KiB PRG bank.
 lda #3
 sta $5100
 lda #$8c
 sta $5114
 lda #$8d
 sta $5115
 lda #$8e
 sta $5116
 lda #$8f
 sta $5117
 ; Horizontal nametable mirroring, 4 KiB CHR windows, no IRQ/split/audio.
 lda #$50
 sta $5105
 lda #1
 sta $5101
 lda #0
 sta $5102
 sta $5103
 sta $5130
 sta $5200
 sta $5204
 sta $5010
 sta $5015
 sta $5123
 lda #2
 sta $5104
 lda #24
 sta $5127
 bit $2002
v1: bit $2002
 bpl v1
 ldx #0
 lda #0
clear:
 sta $0000,x
 sta $0100,x
 sta $0200,x
 sta $0300,x
 sta $0400,x
 sta $0500,x
 sta $0600,x
 sta $0700,x
 inx
 bne clear
v2: bit $2002
 bpl v2
 lda #$00
 sta c_sp
 lda #$08
 sta c_sp+1
 jsr zerobss
 jsr copydata
 jmp _main
.segment "CODE"
_wait_frame:
 lda #1
 sta _ready
@wait:
 lda _ready
 bne @wait
 rts
_pad_read:
 lda #1
 sta $4016
 lda #0
 sta $4016
 ldx #8
@loop:
 pha
 lda $4016
 lsr a
 pla
 rol a
 dex
 bne @loop
 ldx #0
 rts
.export _sprite, _hide
; cc65 fastcall: palette in A, tile/y/x at software-stack offsets 0/1/2.
_sprite:
 ldx _spr
 sta $0202,x
 ldy #0
 lda (c_sp),y
 sta $0201,x
 iny
 lda (c_sp),y
 sta $0200,x
 iny
 lda (c_sp),y
 sta $0203,x
 txa
 clc
 adc #4
 sta _spr
 jmp incsp3
_hide:
 ldx #0
 lda #240
@clear_oam:
 sta $0200,x
 inx
 inx
 inx
 inx
 bne @clear_oam
 stx _spr
 rts
.export _chr_bank
; A is a 4 KiB background frame number. Call with rendering disabled.
_chr_bank:
 sta _art_bank
apply_chr:
 lda _art_bank
 sta $5123
 rts
; Rendering is off. Temporarily expose ExRAM as ordinary CPU RAM to upload it.
_title_extended:
 lda #2
 sta $5104
 ldx #0
@copy:
 lda title_exram,x
 sta $5c00,x
 lda title_exram+$100,x
 sta $5d00,x
 lda title_exram+$200,x
 sta $5e00,x
 lda title_exram+$300,x
 sta $5f00,x
 inx
 bne @copy
 lda #1
 sta _ex_on
 sta $5104
 rts
nmi:
 pha
 txa
 pha
 tya
 pha
 inc _frame
 lda _ready
 bne @render
 jmp @done
@render:
 jsr apply_chr
 ; In 8x8 sprite mode both pattern windows use the $5120-$5127 set.
 lda _sprite_bank
 lsr a
 lsr a
 sta $5127
 lda _ex_on
 bne @extended
 jmp @normal
@extended:
 lda #2
 sta $5104
 .include "../assets/title-anim.inc"
 lda #1
 sta $5104
@normal:
 lda #0
 sta $2003
 lda #2
 sta $4014
 ; Unrolled 96-byte upload costs 768 cycles plus addresses, leaving room
 ; for OAM DMA and portrait ExRAM animation inside NTSC vblank.
 lda _menu_dirty
 bne @menu
 jmp @no_menu
@menu:
 bit $2002
 lda #$21
 sta $2006
 lda #$c0
 sta $2006
 .repeat 32, I
 lda _menu_rows+I
 sta $2007
 .endrepeat
 lda #$23
 sta $2006
 lda #$00
 sta $2006
 .repeat 32, I
 lda _menu_rows+32+I
 sta $2007
 .endrepeat
 lda #$23
 sta $2006
 lda #$40
 sta $2006
 .repeat 32, I
 lda _menu_rows+64+I
 sta $2007
 .endrepeat
 lda #0
 sta _menu_dirty
@no_menu:
 lda _hud_on
 beq @scroll
 bit $2002
 lda #$20
 sta $2006
 lda #$40
 sta $2006
 ldx #0
@hud:
 lda _hud,x
 sta $2007
 inx
 cpx #32
 bne @hud
@scroll:
 lda #0
 sta $2005
 sta $2005
 sta _ready
@done:
 pla
 tay
 pla
 tax
 pla
 rti
irq: rti
.segment "SCENES"
.export _studio, _title, _stage, _plaza
title_exram: .incbin "assets/title.exram"
_studio: .incbin "assets/studio.nam"
_title: .incbin "assets/title.nam"
_stage: .incbin "assets/stage.nam"
_plaza: .incbin "assets/plaza0.nam"
.incbin "assets/plaza1.nam"
.incbin "assets/plaza2.nam"
.segment "RODATA"
.export _districts
_districts: .incbin "assets/district11.nam"
.incbin "assets/district21.nam"
.incbin "assets/district22.nam"
.incbin "assets/district23.nam"
.segment "CHARS"
.incbin "assets/mmc5.chr"
.segment "VECTORS"
.addr nmi, _main_entry, irq
