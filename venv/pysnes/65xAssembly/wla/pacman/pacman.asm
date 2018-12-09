; wla-65816 -o done.obj pacman.asm && wlalink -v -r temp.prj pacman.smc
; adapted from a sample found on http://wiki.superfamicom.org

.include "header.inc"
.include "initsnes.asm"
.include "level.asm"
.include "sprite.asm"
.include "color.asm"
.include "graphics.asm"
.include "video_mode.asm"


.bank 0 slot 0
.org 0
.section "Vblank"
;--------------------------------------
VBlank:
lda $4212	; get joypad status
and #%00000001	; if joy is not ready
bne VBlank	; wait
; Dieses warten ist evtl unklug wenn es laenger als die VBlank phase dauert.
; TODO: Hier mal zur sicherheit ein Counter einbauen

lda $4219	; read joypad: B,Y,Start, up, down, left, right (BYSTudlr) 
sta $0201	; store it
;cmp $0200	; compare it with the previous
;bne +		; if not equal, go
;rti		    ; if it's equal, then return

; insert your button eval code here 
; pacman moving comes now
lda $0201	; get control
and #%00001111	; care about directions
sta $0201	; store this

cmp #%00001000	; up?
bne +		; if not, skip
lda $0101	; get pacman Y Position
cmp #$00	; if on the top,
beq +		; don't do anything
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
; modify pacman sprite
lda #$C0 ; vhppccct
sta $0102
lda #$CE ; Pacman tile
sta $0103
+

lda $0201	; get control
cmp #%00000100	; down?
bne +		; if not, skip
lda $0101   ; get pacman Y Position
cmp #$FF	; if on the bottom, : MOVE LIMIT 
beq +		; don't do anything
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
; modify pacman sprite
lda #$30 ; vhppccct
sta $0102
lda #$CE ; Pacman tile
sta $0103
+

lda $0201	; get control
cmp #%00000010	; left?
bne +		; if not, skip
lda $0100   ; get pacman X Position
cmp #$00	; if on the left,
beq +		; don't do anything
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
; modify pacman sprite
lda #$C0 ; vhppccct
sta $0102
lda #$CC ; Pacman tile
sta $0103
+

lda $0201	; get control
cmp #%00000001	; right?
bne +		; if not, skip
lda $0100   ; get pacman X Position
cmp #$FF	; if on the right, ;MOVE LIMIT
beq +		; don't do anything
inc $0100	; add 1 to X
inc $0100	; add 1 to X
inc $0100	; add 1 to X
inc $0100	; add 1 to X
; modify pacman sprite
lda #$30 ; vhppccct
sta $0102
lda #$CC ; Pacman tile
sta $0103
+

; store old keyboard value to disable the effect of a
; pressed controll stick
;lda $0201
;sta $0200 

sep #%00100000	; 8 bit A
lda $80
sta $2102       ; write at object (OEM Addr) 128
lda $0100		; get our X coord
sta $2104
lda $0101		; get our Y coord
sta $2104
lda $0103       ; Pacman tile
sta $2104
lda $0102       ; vhppccct
sta $2104
rep #%00100000	; get 16 bit A


rti		; F|NisH3D!
;--------------------------------------
.ends

.bank 0 slot 0
.org 0
.section "Main"
;--------------------------------------
Start:
 InitSNES
rep #%00010000	;16 bit xy
sep #%00100000	;8 bit ab

; set pacman start position
lda #$70
sta $0100
lda #$70
sta $0101
lda #$C0 ; vhppccct
sta $0102
lda #$CC ; Pacman tile
sta $0103

JSR PutPaletteInCGRAM
JSR PutTilesInVRAM        ; in graphics.asm
JSR PutLevelTileMapInVRAM ; in level.asm
JSR DrawObject            ; in sprite.asm
JSR InitVideoModeAndBG    ; in video_mode.asm

lda #%10000001	; enable NMI and joypads
sta $4200

forever:
; BG2 besteht vermutlich nur aus PacMan. Hier wird dann
; der gesamte Hintergrund2 einfach nach rechts oder links verschoben.
wai

jmp forever

;--------------------------------------
.ends

.bank 1 slot 0		; We'll use bank 1
.org 0
.section "Tiledata"
.include "tiles.inc"	; If you are using your own tiles, replace this
.ends

.bank 2 slot 0
.org 0
.section "Conversiontable"
VRAMtable:
.db $00,$02,$04,$40,$42,$44,$80,$82,$84
.ends