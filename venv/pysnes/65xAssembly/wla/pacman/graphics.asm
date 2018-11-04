; Bewegt die Grafiken aus unsere tiles.inc in den VRAM
PutTilesInVRAM:
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

RTS