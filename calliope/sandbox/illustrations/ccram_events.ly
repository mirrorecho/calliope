% 2017-08-09 22:59

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "CellA" {
            \set Staff.instrumentName = \markup { CellA }
            \set Staff.shortInstrumentName = \markup { CellA }
            {
                \accidentalStyle modern-cautionary
                a'2
                b'4
                c''8 [
                f'8 ~ ]
                f'4.
                r2
                r8
            }
        }
        \context Staff = "CellA1" {
            \set Staff.instrumentName = \markup { CellA1 }
            \set Staff.shortInstrumentName = \markup { CellA1 }
            {
                \accidentalStyle modern-cautionary
                b'2 -\accent
                cs''4 -\accent
                d''8 -\accent [
                g'8 -\accent ~ ]
                g'4.
                r2
                r8
            }
        }
    >>
}