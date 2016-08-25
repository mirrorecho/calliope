\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\include "/home/randall/Code/mirrorecho/calliope/ly_includes/ametric.ly"

\score {
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
                \timeX
                \time 2/1
                \accidentalStyle neo-modern-cautionary
                \freeOn
                {
                    {
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
                \once \override Staff.TimeSignature #'stencil = ##f 
                \time 2/1
                {
                    {
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
                \timeX
                \time 2/1
                \accidentalStyle neo-modern-cautionary
                \freeOn
                {
                    {
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
                \freeAfter
                \freeOff
                \once \override Staff.TimeSignature #'stencil = ##f 
                \time 2/1
                \freeOn
                {
                    {
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
                \freeAfter
                \freeOff
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
                \timeX
                \time 2/1
                \accidentalStyle neo-modern-cautionary
                \freeOn
                {
                    R1
                    R1
                }
                \once \override Staff.TimeSignature #'stencil = ##f 
                \time 2/1
                {
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
}
