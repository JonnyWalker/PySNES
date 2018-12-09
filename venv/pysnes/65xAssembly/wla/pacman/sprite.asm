DrawObject:

lda #%01100000      ; set sprite size
sta $2101
stz $2102           ; zero data
stz $2103
  
lda #$04 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$CC ; Pacman tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$00 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A8 ; Big Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$30 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$50 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$90 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$B0 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$D0 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$02 ; y
sta $2104
lda #$A8 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$30 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$B0 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$10 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$20 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$20 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; TODO: more
; next line

lda #$00 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$30 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$30 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$B0 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$D0 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$40 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$40 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$50 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$90 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$50 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$60 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$60 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line
lda #$40 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$50 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$90 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$70 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$30 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$B0 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$D0 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$80 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$50 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$90 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$90 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$D0 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$A0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$30 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$B0 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$B0 ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

; next line

lda #$00 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A8 ; Big Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$10 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$20 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$40 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$50 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$60 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$70 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$80 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$90 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$A0 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$C0 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$D0 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A6 ; Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

lda #$E0 ; x
sta $2104
lda #$BE ; y
sta $2104
lda #$A8 ; Big Pill tile
sta $2104
lda #$30 ; vhppccct
sta $2104

RTS