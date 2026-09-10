.export _wait_frame, _pad_read, _main_entry
.export __STARTUP__ : absolute = 1
.export _frame, _ready, _hud, _hud_on, _art_bank, _sprite_bank, _ex_on, _title_extended
.export _menu_dirty, _menu_rows, _status_row, _pause_palette
.import _main, _spr, _mode, _music_act, _paused, _plaza_attrs, zerobss, copydata, incsp3
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
_status_row: .res 32
_pause_palette: .res 32
resource_id: .res 1
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
 .segment "INTROCODE"
_title_extended:
 lda #$81
 sta $5114
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
 lda #$8c
 sta $5114
 rts
.segment "CODE"
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
 cmp #1
 beq @extended
 jmp @normal
@extended:
 lda #2
 sta $5104
 .include "../assets/title-anim.inc"
 lda #1
 sta $5104
@normal:
 ; Musical act lighting changes only during vblank, without stopping the chart.
 lda _paused
 bne @lighting_done
 lda _mode
 cmp #2
 bne @lighting_done
 bit $2002
 lda #$3f
 sta $2006
 lda #$0d
 sta $2006
 ldx _music_act
 lda act_dark,x
 sta $2007
 lda act_mid,x
 sta $2007
 lda act_light,x
 sta $2007
@lighting_done:
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
 ; Context and reactions have a reserved row, above the play field.
 lda #$20
 sta $2006
 lda #$60
 sta $2006
 ldx #0
@status:
 lda _status_row,x
 sta $2007
 inx
 cpx #32
 bne @status
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
act_dark: .byte $04,$01,$06
act_mid: .byte $14,$11,$16
act_light: .byte $34,$31,$36
 ; Intro data lives in PRG bank 0. This loader executes only in the fixed bank,
 ; with rendering/NMI off, and restores bank 12 before returning to C.
.segment "INTROCODE"
.export _load_search_intro
_load_search_intro:
 lda #$80
 sta $5114
 bit $2002
 lda #$20
 sta $2006
 lda #0
 sta $2006
 ldx #0
@nam0:
 lda intro_map,x
 sta $2007
 inx
 bne @nam0
@nam1:
 lda intro_map+$100,x
 sta $2007
 inx
 bne @nam1
@nam2:
 lda intro_map+$200,x
 sta $2007
 inx
 bne @nam2
@nam3:
 lda intro_map+$300,x
 sta $2007
 inx
 bne @nam3
@ex:
 lda intro_exram,x
 sta $5c00,x
 lda intro_exram+$100,x
 sta $5d00,x
 lda intro_exram+$200,x
 sta $5e00,x
 lda intro_exram+$300,x
 sta $5f00,x
 inx
 bne @ex
 lda #$3f
 sta $2006
 lda #0
 sta $2006
@pal:
 lda intro_palette,x
 sta $2007
 inx
 cpx #16
 bne @pal
 lda #$8c
 sta $5114
 lda #2
 sta _ex_on
 lda #1
 sta $5104
 rts
.export _load_resource, _pause_capture, _pause_restore
; Bank 0 holds districts/UI; bank 1 holds the original scenes and title ExRAM.
; Both loaders execute in the fixed bank with NMI/rendering off, then restore
; code bank 12 before returning to C.
_load_resource:
 sta resource_id
 tax
 lda resource_lo,x
 sta ptr1
 lda resource_hi,x
 sta ptr1+1
 lda resource_bank,x
 sta $5114
 bit $2002
 lda #$20
 sta $2006
 lda #0
 sta $2006
 ldx #4
 ldy #0
@page:
 lda (ptr1),y
 sta $2007
 iny
 bne @page
 inc ptr1+1
 dex
 bne @page
 lda resource_id
 cmp #8
 bcs @copy_attrs
 cmp #4
 bcs @mapped
@copy_attrs:
 dec ptr1+1
 ldy #$c0
@attrs:
 lda (ptr1),y
 sta _plaza_attrs,x
 inx
 iny
 bne @attrs
@mapped:
 lda #$8c
 sta $5114
 rts
resource_lo: .lobytes district_maps,district_maps+$400,district_maps+$800,district_maps+$c00,ui_map,_studio,_title,_stage,_plaza,_plaza+$400,_plaza+$800
resource_hi: .hibytes district_maps,district_maps+$400,district_maps+$800,district_maps+$c00,ui_map,_studio,_title,_stage,_plaza,_plaza+$400,_plaza+$800
resource_bank: .byte $80,$80,$80,$80,$80,$81,$81,$81,$81,$81,$81
.segment "BOOTDATA"
.export _studio_floor
_studio_floor: .incbin "assets/studio.nam",648,1
.segment "INTROCODE"
; Pause owns ExRAM only while ordinary nametable rendering is active.
; Snapshot the exact picture, including a live puzzle or a populated district.
_pause_capture:
 bit $2002
 lda #$20
 sta $2006
 lda #0
 sta $2006
 lda $2007
 ldx #0
@save0:
 lda $2007
 sta $5c00,x
 inx
 bne @save0
@save1:
 lda $2007
 sta $5d00,x
 inx
 bne @save1
@save2:
 lda $2007
 sta $5e00,x
 inx
 bne @save2
@save3:
 lda $2007
 sta $5f00,x
 inx
 bne @save3
 lda #$3f
 sta $2006
 lda #0
 sta $2006
@palette:
 lda $2007
 and #$3f
 sta _pause_palette,x
 inx
 cpx #32
 bne @palette
 rts
_pause_restore:
 bit $2002
 lda #$20
 sta $2006
 lda #0
 sta $2006
 ldx #0
@copy0:
 lda $5c00,x
 sta $2007
 inx
 bne @copy0
@copy1:
 lda $5d00,x
 sta $2007
 inx
 bne @copy1
@copy2:
 lda $5e00,x
 sta $2007
 inx
 bne @copy2
@copy3:
 lda $5f00,x
 sta $2007
 inx
 bne @copy3
 lda #$3f
 sta $2006
 lda #0
 sta $2006
@palette:
 lda _pause_palette,x
 sta $2007
 inx
 cpx #32
 bne @palette
 rts
.segment "INTRODATA"
intro_map: .incbin "assets/dany-intro.nam"
intro_exram: .incbin "assets/dany-intro.exram"
intro_palette: .incbin "assets/dany-intro.pal"
.segment "SCENES"
.export _studio, _title, _stage, _plaza
title_exram: .incbin "assets/title.exram"
_studio: .incbin "assets/studio.nam"
_title: .incbin "assets/title.nam"
_stage: .incbin "assets/stage.nam"
_plaza: .incbin "assets/plaza0.nam"
.incbin "assets/plaza1.nam"
.incbin "assets/plaza2.nam"
.segment "PRESENTATIONDATA"
district_maps: .incbin "assets/district11.nam"
.incbin "assets/district21.nam"
.incbin "assets/district22.nam"
.incbin "assets/district23.nam"
ui_map: .incbin "assets/presentation.nam"
.segment "CHARS"
.incbin "assets/mmc5.chr"
.segment "VECTORS"
.addr nmi, _main_entry, irq
