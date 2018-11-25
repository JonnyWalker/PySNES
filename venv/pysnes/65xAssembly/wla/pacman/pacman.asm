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

lda $4219	; read joypad (BYSTudlr)
sta $0201	; store it
cmp $0200	; compare it with the previous
bne +		; if not equal, go
rti		    ; if it's equal, then return

stz $0100	; delete the scroll
stz $0101	; data also

++		; now for Y
cmp #%01000000	; Y?
bne +		; no, jump forward (this should not happen)
; Y is pressed, write an X ($0A)
lda $0101	; get Y
sta $0202	; put it to a temp value
clc
adc $0202	; multiply by 3 - an easy way
adc $0202	; A*3=A+A+A : )
adc $0100	; add X
; Now A contains our address
ldx #$0000	; be on the safe side
tax
lda #$0A
sta $0000,x	; put $0A to the good address
+		; finished putting tiles

; cursor moving comes now
lda $0201	; get control
and #%00001111	; care about directions
sta $0201	; store this

cmp #%00001000	; up?
bne +		; if not, skip
lda $0101	; get scroll Y
cmp #$00	; if on the top,
beq +		; don't do anything
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
dec $0101	; sub 1 from Y
+

lda $0201	; get control
cmp #%00000100	; down?
bne +		; if not, skip
lda $0101
cmp #$FF	; if on the bottom, : MOVE LIMIT 
beq +		; don't do anything
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
inc $0101	; add 1 to Y
+

lda $0201	; get control
cmp #%00000010	; left?
bne +		; if not, skip
lda $0100
cmp #$00	; if on the left,
beq +		; don't do anything
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
dec $0100	; sub 1 from X
+

lda $0201	; get control
cmp #%00000001	; right?
bne +		; if not, skip
lda $0100
cmp #$FF	; if on the right, ;MOVE LIMIT
beq +		; don't do anything
inc $0100	; add 1 to X
inc $0100	; add 1 to X
inc $0100	; add 1 to X
inc $0100	; add 1 to X
+

sep #%00100000	; 8 bit A
stz $2102
stz $2103  
lda $0100		; get our X coord
sta $2104
lda $0101		; get our Y coord
sta $2104
lda #$CC ; Pacman tile
sta $2104
lda #$30 ; vhppccct
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