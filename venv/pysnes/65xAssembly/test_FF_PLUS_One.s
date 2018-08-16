; Displays green WHEN FF+1 is zero (8Bit mode)
;
; ca65 test_FF_PLUS_One.s
; ld65 -C lorom128.cfg -o test_FF_PLUS_One.smc test_FF_PLUS_One.0

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

; RELEVANT PART
    lda #$FF
    inc
    beq green ; jump to green if FF+1 is zero
; END PART

    ; Set background color to red ($001F)
    lda #$1F
    sta $2122
    lda #$00
    sta $2122

    ; Maximum screen brightness
    lda #$0F
    sta $2100

    jmp forever

green:
    ; Set background color to green ($03E0)
    lda #$E0
    sta $2122
    lda #$03
    sta $2122

    ; Maximum screen brightness
    lda #$0F
    sta $2100

forever:
    jmp forever