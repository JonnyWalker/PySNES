; Sets up processor basics and ROM headers/vectors

.p816   ; 65816 processor
.i16    ; X/Y are 16 bits
.a8     ; A is 8 bits

.segment "HEADER"     ; +$7FE0 in file
    .byte ROM_NAME

.segment "ROMINFO"    ; +$7FD5 in file
    .byte $30         ; LoROM, fast-capable
    .byte 0           ; no battery RAM
    .byte $07         ; 128K ROM
    .byte 0,0,0,0
    .word $AAAA,$5555 ; dummy checksum and complement

.segment "VECTORS"
    .word 0, 0, 0, 0, 0, 0, 0, 0
    .word 0, 0, 0, 0, 0, 0, reset, 0

.code

.macro init_cpu
    clc
    xce
    rep #$10        ; X/Y 16-bit
    sep #$20        ; A 8-bit
.endmacro