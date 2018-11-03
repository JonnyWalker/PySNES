; wla-65816 -o done.obj pacman.asm && wlalink -v -r temp.prj pacman.smc
; adapted from a sample found on http://wiki.superfamicom.org

.include "header.inc"
.include "initsnes.asm"

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

ldx #$0000
- lda Palette.l,x
sta $2122
inx
cpx #24
bne -

; Hier wird die Palette noch mal fuer BG2  geladen
lda #32
sta $2121
ldx #$0000
- lda Palette.l,x
sta $2122
inx
cpx #24
bne -


ldx #TileData	; Address
lda #:TileData	; of UntitledData
ldy #(128*16*4)	; length of data - witulski: 64 Tiles, 16 Breite und 4 Bit fuer Farbe
stx $4302	; write
sta $4304	; address
sty $4305	; and length
lda #%00000001	; set this mode (transferring words)
sta $4300
lda #$18	; $211[89]: VRAM data write
sta $4301	; set destination

ldy #$0000	; Write to VRAM from $0000
sty $2116

lda #%00000001	; start DMA, channel 0
sta $420B
lda #%10000000	; VRAM writing mode
sta $2115
ldx #$4000	; write to vram
stx $2116	; from $4000

;ugly code starts here - it writes the # shape I mentioned before.
; witulski: Man packt den Index der Tile in x und laed das Ganze in 2118.
; das zeichnet dann (spaeter) die Tile. Es wird hier einfach von links nach rechts und
; von oben nach unten gezeichent

; Zeichne Labyrinth

;Line 0: r------7r------7
ldx #$000A	; tile (r)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (7) TODO
stx $2118
ldx #$000C	; tile (r) TODO
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000C	; tile (-)
stx $2118
ldx #$000E	; tile (7)
stx $2118

; Dies macht die Zeile mit leeren Grafiken voll
; Nur die halbe Zeile ist auf dem Monitor sichtbar
; Da wir nicht scrollen koennte man hier ein bel. Tile nehmen.
ldx #$0000 ; tile 0 (leer)
.rept 16
 stx $2118	 
.endr

;Line 2: |G G    LJ     |
ldx #$0008	; (|) 
stx $2118
ldx #$0046	; Kirsche 
stx $2118
ldx #$0048	; Erdbeere 
stx $2118
ldx #$004A	; Birne 
stx $2118
ldx #$004C	; Pacman 
stx $2118
ldx #$004E  ; Pacman (unten)
stx $2118
ldx #$0060	; nix
stx $2118
ldx #$0060	; nix
stx $2118
ldx #$0062	; 
stx $2118
ldx #$0064	; Geist (hellblau)
stx $2118
ldx #$0066	; Geist (pink)
stx $2118
ldx #$0068	; Geist (rot)
stx $2118
ldx #$006A	; Geist (orange)
stx $2118
ldx #$006C	; Trans-Gender-Fluid PacMan (ok ok.. es ist Mrs PacMan)
stx $2118
ldx #$006E  ; Trans-Gender-Fluid PacMan (ok ok.. es ist Mrs PacMan)
stx $2118
ldx #$0028	; tile (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 3: |              |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 4: |              |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 5: L__7        r__J
ldx #$002A	; tile (L)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$0024	; tile 0 (7)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0026	; tile 0 (r)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002E	; tile 0 (J)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 6:    |        |
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0008	; tile 0 (|)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 7: ___J        L___
ldx #$000C	; tile 4 (-)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000C	; tile 4 (-)
stx $2118
ldx #$0004	; tile 0 (J)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0006	; tile 0 (L)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 8: L__7        r__J
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$0024	; tile 0 (7)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0026	; tile 0 (r)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 09:    |        |
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0008	; tile 0 (|)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 10: ___J        L___
ldx #$000A	; tile 4 (r)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000C	; tile 4 (-)
stx $2118
ldx #$0004	; tile 0 (J)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0006	; tile 0 (L)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000C	; tile 0 (-)
stx $2118
ldx #$000E	; tile 0 (7)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 11: |              |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 12: |              |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 13: |              |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 14: L__7        r__J
ldx #$002A	; tile 4 (L)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002E	; tile 0 (J)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

ldx #$6000	; BG2 will start here
stx $2116
ldx #$004C	; Tile-Nummer $4C, (und $4D, $5C, $5D): PacMan
stx $2118
;ldx #$0002	; tile 0 (r)
;stx $2118
;set up the screen
; witulski: Bit 0-2: mode 0-7 (mode 0 wird gewaehlt und kennt 4 BG layer)
;           Bit 3:   Wenn auf 1 dann ist BG3 immer vor allem 
;           Bit 4:   Wenn 0, 8x8 Tiles in BG1, sonst 16x16 Tiles
;           Bit 5:   Wenn 0, 8x8 Tiles in BG2, sonst 16x16 Tiles
;           Bit 6:   Wenn 0, 8x8 Tiles in BG3, sonst 16x16 Tiles
;           Bit 7:   Wenn 0, 8x8 Tiles in BG4, sonst 16x16 Tiles
;           Ein laden in das screen mode PPU register ($2105) 
;           setzt den mode und tile Groesse
lda #%00110001	; 16x16 tiles, Mode 1
sta $2105	; screen mode register
; witulski: Das BG1SC Register ($2107) setzt die Daten fuer das BG1 Layer
;           Bit 0-1: Groesse des Hintergrundes
;           Bit 2-7: Startadresse im VRAM der Tilemap fuer diesen Hintergrund
;           fuer mich ist das eigentlich ne 16 (aber irgendwie ist es ne $4000)
lda #%01000000	; data starts from $4000
sta $2107	; for BG1
; witulski: Das BG2SC Register ($2108) setzt die Daten fuer das BG2 Layer
;           Bit 0-1: Groesse des Hintergrundes
;           Bit 2-7: Startadresse im VRAM der Tilemap fuer diesen Hintergrund
;           fuer mich ist das eigentlich ne 24 (aber irgendwie ist es ne $6000)
lda #%01100000	; and $6000
sta $2108	; for BG2
; witulski: Hier kann ich sagen wo die Grafiken fuer die Tilemap im speicher liegen
;           wir haben die vorhin einfach an den Anfang gepackt, also passt 0000
stz $210B	; BG1 and BG2 use the $0000 tiles
; witulski: Einscheide welche BGs auf dem Main Screen liegen sollen
;           Bit 0: BG1
;           Bit 1: BG2
;           Bit 2: BG3
;           Bit 3: BG4
;           Bit 4: OBJ (also die beweglichen Sprites) - nutzen wir nicht
lda #%00000011	; enable bg1&2
sta $212C

;The PPU doesn't process the top line, so we scroll down 1 line.
rep #$20	; 16bit a
lda #$07FF	; this is -1 for BG1
sep #$20	; 8bit a
sta $210E	; BG1 vert scroll
xba
sta $210E

rep #$20	; 16bit a
lda #$FFFF	; this is -1 for BG2
sep #$20	; 8bit a
sta $2110	; BG2 vert scroll
xba
sta $2110

lda #%00001111	; enable screen, set brightness to 15
sta $2100

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
; witulski: Hier wird irgendwie mit 9 schwarzen Feldern uebermalt. ohne diesen
; Code ist PacMan im Hintergrund. bzw mit einem X oder O?
;--------------------------------------
;ldx #$0000		; reset our counter
; 
;-
;rep #%00100000		; 16 bit A
;lda #$0000		; empty it
;sep #%00100000		; 8 bit a
;lda VRAMtable.l,x	; this is a long indexed address, nice : )
;rep #%00100000
;clc
;adc #$4000		; add $4000 to the value
;sta $2116		; write to VRAM from here
;lda #$0000		; reset A while it's still 16 bit
;sep #%00100000		; 8 bit A
;lda $0000,x		; get the corresponding tile from RAM
;; VRAM data write mode is still %10000000
;sta $2118		; write
;stz $2119		; this is the hi-byte
;inx
;cpx #9			; finished?
;bne -			; no, go back
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