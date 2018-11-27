DrawObject:

lda #%01100000      ; set sprite size
sta $2101
stz $2102           ; zero data
stz $2103  
lda #$00 ; x
sta $2104
lda #$00 ; y
sta $2104
lda #$CC ; Pacman tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$04 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$14 ; x
sta $2104
lda #$04 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$18 ; x
sta $2104
lda #$04 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$1C ; x
sta $2104
lda #$04 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

RTS