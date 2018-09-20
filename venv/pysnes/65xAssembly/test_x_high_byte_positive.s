; Displays green when sep/rep reset the high byte of X
;
; ca65 test_x_high_byte_positive.s
; ld65 -C lorom128.cfg -o test_x_high_byte_positive.smc test_x_high_byte_positive.o

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
	.a16
	; change to 16 bit mode
	clc	
	xce
	; set A to 16 bit
	rep #$20
	lda #$1100
	; set A to 8 and back to 16
	sep #$20
	rep #$20
	and #$1100
	beq green
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