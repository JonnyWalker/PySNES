; Displays green screen
;
; ca65 green.s
; ld65 -C lorom128.cfg -o green.smc green.o

.define ROM_NAME "GREEN"
.include "lorom128.inc"

reset:
    init_cpu

    ; Clear PPU registers
    ldx #$33
@loop:  stz $2100,x
    stz $4200,x
    dex
    bpl @loop

    ; Set background color to $03E0
    lda #$E0
    sta $2122
    lda #$03
    sta $2122

    ; Maximum screen brightness
    lda #$0F
    sta $2100

forever:
    jmp forever