; Laed die Farben in den Farbspeicher
PutPaletteInCGRAM:

ldx #$0000
- lda Palette.l,x
sta $2122
inx
cpx #512
bne -

RTS