; Kurzbeschreibung: Level Zeichnen (Das Labyrinth)
;
; Diese ASM Datei schreibt die Tilemap fuer das Level in 
; den Bildspeicher
; Man packt den Index der Tile in x und laed das Ganze in 2118.
; Dies zeichnet dann (spaeter) die Tile. 
; Es wird hier einfach von links nach rechts und
; von oben nach unten gezeichnet, wobei die Haelfte des Bildschirms
; nicht Sichtbar ist (sowas kann man fuer Sidescroller  wie Mario nutzen)

PutLevelTileMapInVRAM:
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

RTS ; Jump Back to call-side