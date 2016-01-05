\language english
\include "/home/randall/Code/mirrorecho/calliope/ly_material/ametric.ly"
\new Score <<
    \context Staff = "l1" {
        \set Staff.instrumentName = \markup { L1 }
        \set Staff.shortInstrumentName = \markup { L1 }
        {
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                \tempo 4=120
                bf4
                bf'4
                c'4
                bf4
            }
            {
                {
                    {
                        \once \override 
                                            Staff.TimeSignature #'stencil = #(lambda (grob)
                                            (parenthesize-stencil (grob-interpret-markup grob 
                                            (markup #:override '(baseline-skip . 0.5) #:column ("X" "X"))
                                            ) 0.1 0.4 0.4 0.1 ))
                                            
                        \time 2/1
                        \bar "||"
                        \accidentalStyle neo-modern-cautionary
                        \tempo "Freely,  10'' ca"
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                    {
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                    {
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                }
                {
                    c'8 (
                    cs'8
                    d'8
                    ef'8 )
                }
            }
            {
                {
                    {
                        \once \override Staff.TimeSignature #'stencil = ##f 
                        \time 2/1
                        \bar "!"
                        \tempo " 10'' ca"
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                    {
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                    {
                        f'8 (
                        df'8
                        f'8
                        c'8 )
                    }
                }
                {
                    c'8 (
                    cs'8
                    d'8
                    ef'8 )
                }
            }
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                bf4
                bf'4
                c'4
                bf4
            }
        }
    }
    \context Staff = "l2" {
        \set Staff.instrumentName = \markup { L2 }
        \set Staff.shortInstrumentName = \markup { L2 }
        {
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                \tempo 4=120
                c'1
            }
            {
                {
                    \once \override 
                                        Staff.TimeSignature #'stencil = #(lambda (grob)
                                        (parenthesize-stencil (grob-interpret-markup grob 
                                        (markup #:override '(baseline-skip . 0.5) #:column ("X" "X"))
                                        ) 0.1 0.4 0.4 0.1 ))
                                        
                    \time 2/1
                    \bar "||"
                    \accidentalStyle neo-modern-cautionary
                    \tempo "Freely,  10'' ca"
                    a8 (
                    b8
                    c'8
                    e'8 )
                }
                {
                    a32
                    r1 -\fermata
                }
                s32 * 15
            }
            {
                {
                    \once \override Staff.TimeSignature #'stencil = ##f 
                    \time 2/1
                    \bar "!"
                    \tempo " 10'' ca"
                    a8 (
                    b8
                    c'8
                    e'8 )
                }
                {
                    a32
                    r1 -\fermata
                }
                s32 * 15
            }
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                c'1
            }
        }
    }
    \context Staff = "l3" {
        \set Staff.instrumentName = \markup { L3 }
        \set Staff.shortInstrumentName = \markup { L3 }
        {
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                \tempo 4=120
                R1
            }
            {
                \once \override 
                                    Staff.TimeSignature #'stencil = #(lambda (grob)
                                    (parenthesize-stencil (grob-interpret-markup grob 
                                    (markup #:override '(baseline-skip . 0.5) #:column ("X" "X"))
                                    ) 0.1 0.4 0.4 0.1 ))
                                    
                \time 2/1
                \bar "||"
                \accidentalStyle neo-modern-cautionary
                \tempo "Freely,  10'' ca"
                R1
                R1
            }
            {
                \once \override Staff.TimeSignature #'stencil = ##f 
                \time 2/1
                \bar "!"
                \tempo " 10'' ca"
                R1
                R1
            }
            {
                \numericTimeSignature
                \time 4/4
                \bar "||"
                \accidentalStyle modern-cautionary
                R1
            }
        }
    }
>>