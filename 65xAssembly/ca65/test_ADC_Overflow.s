; Only the bin encoding is needed. 
;
; ca65 test_ADC_Overflow.s
; ld65 -C lorom128.cfg -o test_ADC_Overflow.smc test_ADC_Overflow.o

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
    lda #$7F  ; MAX_INT
    adc #$01  ; MAX_INT+1 => overflow => v flag set
    bvs green ; branch green if v flag is set
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