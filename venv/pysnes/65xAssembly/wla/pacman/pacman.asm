; wla-65816 -o done.obj pacman.asm && wlalink -v -r temp.prj pacman.smc
; adapted from a sample found on http://wiki.superfamicom.org

.include "header.inc"
.include "initsnes.asm"
.include "level.asm"
.include "color.asm"
.include "graphics.asm"
.include "video_mode.asm"

.macro ConvertX
; Data in: our coord in A
; Data out: SNES scroll data in C (the 16 bit A)
.rept 5
asl a		; multiply A by 32
.endr
rep #%00100000	; 16 bit A
eor #$FFFF	; this will do A=1-A
inc a		; A=A+1
sep #%00100000	; 8 bit A
.endm

.macro ConvertY
; Data in: our coord in A
; Data out: SNES scroll data in C (the 16 bit A)
.rept 5
asl a		; multiply A by 32
.endr
rep #%00100000	; 16 bit A
eor #$FFFF	; this will do A=1-A
sep #%00100000	; 8 bit A
.endm

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

+ sta $0200	; store
and #%00010000	; get the start button
		; this will be the delete key
beq +		; if it's 0, we don't have to delete
ldx #$0000
- stz $0000,x	; delete addresses $0000 to $0008
inx
cpx #$09	; this is 9. Guess why (homework : ) )
bne -
stz $0100	; delete the scroll
stz $0101	; data also

+ lda $0201	; get back the temp value
and #%11000000	; Care only about B and Y
beq +		; if empty, skip this
; so, B or Y is pressed. Let's say B is O,
; and Y is X.
cmp #%11000000	; both are pressed?
beq +		; then don't do anything
cmp #%10000000	; B?
bne ++		; no, try Y
; B is pressed, write an O ($08)
; we have to tell the cursor position,
; and calculate an address from that
; Formula: Address=3*Y+X
lda $0101	; get Y
sta $0202	; put it to a temp value
clc
adc $0202	; multiply by 3 - an easy way
adc $0202	; A*3=A+A+A : )
adc $0100	; add X
; Now A contains our address
ldx #$0000	; be on the safe side
tax
lda #$08
sta $0000,x	; put $08 to the good address
jmp +		; done with this

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
+

lda $0201	; get control
cmp #%00000100	; down?
bne +		; if not, skip
lda $0101
cmp #$02	; if on the bottom,
beq +		; don't do anything
inc $0101	; add 1 to Y
+

lda $0201	; get control
cmp #%00000010	; left?
bne +		; if not, skip
lda $0100
cmp #$00	; if on the left,
beq +		; don't do anything
dec $0100	; sub 1 from X
+

lda $0201	; get control
cmp #%00000001	; right?
bne +		; if not, skip
lda $0100
cmp #$02	; if on the right,
beq +		; don't do anything
inc $0100	; add 1 to X
+
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
JSR InitVideoModeAndBG    ; in video_mode.asm

lda #%10000001	; enable NMI and joypads
sta $4200

forever:
; BG2 besteht vermutlich nur aus PacMan. Hier wird dann
; der gesamte Hintergrund2 einfach nach rechts oder links verschoben.
wai
rep #%00100000	; get 16 bit A
lda #$0000		; empty it
sep #%00100000	; 8 bit A
lda $0100		; get our X coord
 ConvertX		; WLA needs a space before a macro name
sta $210F		; BG2 horz scroll
xba
sta $210F		; write 16 bits

;now repeat it, but change $0100 to $0101, and $210F to $2110
rep #%00100000	; get 16 bit A
lda #$0000		; empty it
sep #%00100000	; 8 bit A
lda $0101		; get our Y coord
 ConvertY		; WLA needs a space before a macro name
sta $2110		; BG2 vert scroll
xba
sta $2110		; write 16 bits

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