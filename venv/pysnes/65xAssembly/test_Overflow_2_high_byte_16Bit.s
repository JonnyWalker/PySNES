; Displays green WHEN FF+1 is zero (16Bit mode) - It is not
;
; ca65 test_Overflow_2_high_byte.s 
; ld65 -C lorom128.cfg -o test_Overflow_2_high_byte.smc test_Overflow_2_high_byte.o

.define ROM_NAME "RED"
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
    REP #$20  ; A 16-bit
    .a16
    lda #$FF
    inc
    REP #$01  ; clear Z Flag
    CMP #$0000
    beq green ; jump to green if A is zero. 
    ; This means FF+1 in 16Bit Mode does not write the high byte in 16 Bit Mode!
    ; In 16 Bit Mode INC of x00FF is x0100!
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