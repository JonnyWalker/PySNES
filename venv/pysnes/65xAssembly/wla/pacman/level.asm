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
;Line 0: r------||------7
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
ldx #$0060	; tile (||) 
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
ldx #$0000	; tile (leer)
stx $2118

; Dies macht die Zeile mit leeren Grafiken voll
; Nur die halbe Zeile ist auf dem Monitor sichtbar
; Da wir nicht scrollen koennte man hier ein bel. Tile nehmen.
ldx #$0000 ; tile 0 (leer)
.rept 16
 stx $2118	 
.endr

;Line 2: | <> <> || <> <> |
ldx #$0008	; (|) 
stx $2118
ldx #$004C	; < 
stx $2118
ldx #$004E	; > 
stx $2118
ldx #$0000	;  
stx $2118
ldx #$004C	; < 
stx $2118
ldx #$004E  ; >
stx $2118
ldx #$0000	; 
stx $2118
ldx #$0048	; ||
stx $2118
ldx #$0000	; 
stx $2118
ldx #$004C	; <
stx $2118
ldx #$004E	; >
stx $2118
ldx #$0000	; 
stx $2118
ldx #$004C	; <
stx $2118
ldx #$004E  ; >
stx $2118
ldx #$0028	; tile (|)
stx $2118
ldx #$0000	; tile (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 3: |       U       |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$00CA	; tile  (leer)
stx $2118
ldx #$00C8	; tile  (leer)
stx $2118
ldx #$00C6	; tile  (leer)
stx $2118
ldx #$00E2	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$006A	; tile  (U)
stx $2118
ldx #$00E4	; tile  (Geist)
stx $2118
ldx #$00E6	; tile  (blauer Geist)
stx $2118
ldx #$00E8	; tile  (pinker Geist)
stx $2118
ldx #$00EA	; tile  (roter Geist)
stx $2118
ldx #$00EC	; tile  (oranger Geist)
stx $2118
ldx #$00EE	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 4: |<=> n   n <=> |
ldx #$0008	; tile (|)
stx $2118
ldx #$004C	; tile  (<)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$004E	; tile  (>)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$004A	; tile  (n)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$004A	; tile  (n)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$004C	; tile  (<)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$004E	; tile  (>)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 5: |    L> <J    |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile (leer)
stx $2118
ldx #$0000	; tile (leer)
stx $2118
ldx #$0000	; tile (leer)
stx $2118
ldx #$0000	; tile (leer)
stx $2118
ldx #$0064	; tile 0 (L)
stx $2118
ldx #$004E	; tile 0 (>)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$004C	; tile 0 (<)
stx $2118
ldx #$0066	; tile 0 (J)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 6: ===>       <===
ldx #$0022	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0024	; tile  (>)
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
ldx #$0026	; tile  (<)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 7:       <===>      
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
ldx #$004C	; tile  (<)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$004E	; tile  (>)
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

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 8: ===>       <===
ldx #$0002	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0024	; tile  (>)
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
ldx #$0026	; tile  (r)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0020	; tile  (=)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 09: |     <===>      |
ldx #$0008	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$004C	; tile 0 (<)
stx $2118
ldx #$006E	; tile 0 (=)
stx $2118
ldx #$006E	; tile 0 (=)
stx $2118
ldx #$006E	; tile 0 (=)
stx $2118
ldx #$004E	; tile 0 (>)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0028	; tile 0 (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 10: | <=\   o   /=> |
ldx #$0008	; tile 4 
stx $2118
ldx #$004C	; tile 0 (<)
stx $2118
ldx #$006E	; tile 0 (=)
stx $2118
ldx #$0046	; tile 0 (\)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$006C	; tile 0 (o)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0000	; tile 0 (leer)
stx $2118
ldx #$0044	; tile 0 (/)
stx $2118
ldx #$006E	; tile 0 (=)
stx $2118
ldx #$004E	; tile 0 (>)
stx $2118
ldx #$0028	; tile 0 (7)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 11: |  u n    n u  |
ldx #$0008	; tile (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$006A	; tile  (u)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$004A	; tile  (n)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$004A	; tile  (n)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$006A	; tile  (u)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 12: |o   L===J   o|
ldx #$0008	; tile (|)
stx $2118
ldx #$006C	; tile 0 (o)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0064	; tile  (L)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$006E	; tile  (=)
stx $2118
ldx #$0066	; tile  (J)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118
ldx #$006C	; tile 0 (o)
stx $2118
ldx #$0028	; tile  (|)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

;Line 13: L__n_______n__J
ldx #$002A	; tile 4 (L)
stx $2118
ldx #$002C	; tile 0 (-)
stx $2118
ldx #$002C	; tile 4 (-)
stx $2118
ldx #$0040	; tile  (n)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$0040	; tile  (n)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002C	; tile  (-)
stx $2118
ldx #$002E	; tile  (J)
stx $2118
ldx #$0000	; tile  (leer)
stx $2118

ldx #$0000
.rept 16
 stx $2118
.endr

ldx #$0000
.rept 32
 stx $2118
.endr

ldx #$6000	; BG2 will start here
stx $2116
.rept 256
 stx $2118
.endr
.rept 128
 stx $2118
.endr
.rept 32
 stx $2118
.endr
ldx #$00C0	; tile  (leer)
stx $2118
ldx #$00C2	; tile  (leer)
stx $2118
ldx #$00C4	; tile  (leer)
stx $2118
ldx #$0000


RTS ; Jump Back to call-side