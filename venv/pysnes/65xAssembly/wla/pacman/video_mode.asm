InitVideoModeAndBG:

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
lda #%00010011	; enable bg1&2&obj
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

RTS