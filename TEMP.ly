\header{title = "a"} 

staff = \new Staff{{
    \key c \major 
    \set Staff.instrumentName = "Piano" 
    \time 4/4 

    c''8 c''8 g''8 g''8 a''8 a''8 g''8 g''8 f''8 f''8 e''8 e''8 d''8 d''8 c''4 g''8 g''8 f''8 f''8 e''8 e''8 d''8 d''8 g''8 g''8 f''8 f''8 e''8 e''8 d''8 d''8 c''8 c''8 g''8 g''8 a''8 a''8 g''8 g''8 f''8 f''8 e''8 e''8 d''8 d''8 c'''4  
    \bar "|."
    }
}

\score{
    \staff
}