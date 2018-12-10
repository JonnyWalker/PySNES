DrawObject:

lda #%01100000      ; set sprite size
sta $2101
stz $2102           ; zero data
stz $2103
  
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

; 120 Pills

; now pacman and ghosts
lda $80
sta $2102           ; write at object (OEM Addr) 128


lda $0100 ; x
sta $2104
lda $0101 ; y
sta $2104
lda $0103 ; Pacman tile
sta $2104
lda $0102 ; vhppccct
sta $2104

lda $0104 ; x
sta $2104
lda $0105 ; y
sta $2104
lda $0107 ; Mrs Pacman tile
sta $2104
lda $0106 ; vhppccct
sta $2104

lda #$20  ; x
sta $2104
lda #$A0  ; y
sta $2104
lda #$E4  ; blauer Geist tile
sta $2104
lda #$30  ; vhppccct
sta $2104

lda #$C0  ; x
sta $2104
lda #$A0  ; y
sta $2104
lda #$E6  ; pinker Geist tile
sta $2104
lda #$30  ; vhppccct
sta $2104

lda #$C0  ; x
sta $2104
lda #$02  ; y
sta $2104
lda #$E8  ; roter Geist tile
sta $2104
lda #$30  ; vhppccct
sta $2104

lda #$20  ; x
sta $2104
lda #$02  ; y
sta $2104
lda #$EA  ; oranger Geist tile
sta $2104
lda #$30  ; vhppccct
sta $2104

RTS