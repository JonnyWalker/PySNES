TileData:
    ; GhostUL.bmp
    .db $00,$00,$00,$03,$00,$0f,$00,$1f,$06,$3f,$0f,$3f,$0f,$3c,$0f,$7c
    ; GhostUR.bmp
    .db $00,$00,$00,$c0,$00,$f0,$00,$f8,$18,$fc,$3c,$fc,$3c,$f0,$3c,$f2
    ; GhostLR.bmp
    .db $18,$fe,$00,$fe,$00,$fe,$00,$fe,$00,$fe,$00,$76,$00,$62,$00,$00
    ; GhostLL.bmp
    .db $06,$7f,$00,$7f,$00,$7f,$00,$7f,$00,$7f,$00,$6e,$00,$46,$00,$00

    ; Ghost2LL.bmp
    .db $7f,$00,$7f,$00,$7f,$19,$7f,$26,$7f,$00,$6e,$00,$46,$00,$00,$00
    ; Ghost2LR.bmp
    .db $fe,$00,$fe,$00,$fe,$98,$fe,$64,$fe,$00,$76,$00,$62,$00,$00,$00
    ; Ghost2UL.bmp
    .db $00,$00,$03,$00,$0f,$00,$1f,$00,$3f,$00,$3f,$00,$3f,$06,$7f,$06
    ; Ghost2UR.bmp
    .db $00,$00,$c0,$00,$f0,$00,$f8,$00,$fc,$00,$fc,$00,$fc,$60,$fe,$60

    ; PacManUL.bmp
    .db $00,$00,$03,$03,$0f,$0f,$1f,$1f,$1f,$1f,$3f,$3f,$3f,$3f,$3e,$3e
    ; PacManUR.bmp
    .db $00,$00,$e0,$e0,$f8,$f8,$fc,$fc,$fc,$fc,$f0,$f0,$80,$80,$00,$00
    ; PacManLR.bmp
    .db $80,$80,$f0,$f0,$fc,$fc,$fc,$fc,$f8,$f8,$e0,$e0,$00,$00,$00,$00
    ; PacManLL.bmp
    .db $3f,$3f,$3f,$3f,$1f,$1f,$1f,$1f,$0f,$0f,$03,$03,$00,$00,$00,$00

Palette0:
    .db $00,$00,$00,$7c,$1f,$00,$ff,$7f
Palette1:
    .db $00,$00,$00,$7c,$1f,$00,$ff,$03