% 2017-06-25 17:56

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "c1" {
            \set Staff.instrumentName = \markup { C1 }
            \set Staff.shortInstrumentName = \markup { C1 }
            {
                {
                    \accidentalStyle modern-cautionary
                    bf4
                    a'2
                    r4
                    r8
                    a'8
                    r2.
                    r1
                    r1
                }
            }
        }
        \context Staff = "c2" {
            \set Staff.instrumentName = \markup { C2 }
            \set Staff.shortInstrumentName = \markup { C2 }
            {
                {
                    \accidentalStyle modern-cautionary
                    r4
                    c2
                    c'4 ~
                    c'8 [
                    a'8 ]
                    r2.
                    r1
                    r1
                }
            }
        }
    >>
}