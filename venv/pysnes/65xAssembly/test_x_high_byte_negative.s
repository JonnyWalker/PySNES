; Displays red to show that x + 1 - 1 is indeed not 0 without switching from 8 bit and back.
;
; ca65 test_x_high_byte_negative.s
; ld65 -C lorom128.cfg -o test_x_high_byte_negative.smc test_x_high_byte_negative.0

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
	.i16
	; change to 16 bit mode
	clc	
	xce
	; set X to 16 bit
	rep #$10
	ldx #$1100
	; set X to 8 and back to 16
	;sep #$10
	;rep #$10
	; since we didnt change from 8 to 16 X + 1 - 1 should not be zero
	inx
	dex
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