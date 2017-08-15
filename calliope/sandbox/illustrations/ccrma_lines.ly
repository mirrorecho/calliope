% 2017-08-11 18:21

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "line0" {
            \set Staff.instrumentName = \markup { Line0 }
            \set Staff.shortInstrumentName = \markup { Line0 }
            {
                \accidentalStyle modern-cautionary
                c'1
                d'1
            }
        }
        \context Staff = "line1" {
            \set Staff.instrumentName = \markup { Line1 }
            \set Staff.shortInstrumentName = \markup { Line1 }
            {
                \accidentalStyle modern-cautionary
                e'1
                f'1
            }
        }
        \context Staff = "line2" {
            \set Staff.instrumentName = \markup { Line2 }
            \set Staff.shortInstrumentName = \markup { Line2 }
            {
                \accidentalStyle modern-cautionary
                e'1
                f'1
            }
        }
        \context Staff = "line3" {
            \set Staff.instrumentName = \markup { Line3 }
            \set Staff.shortInstrumentName = \markup { Line3 }
            {
                \accidentalStyle modern-cautionary
                e'1
                f'1
            }
        }
        \context Staff = "line4" {
            \set Staff.instrumentName = \markup { Line4 }
            \set Staff.shortInstrumentName = \markup { Line4 }
            {
                \accidentalStyle modern-cautionary
                e'1
                f'1
            }
        }
        \context Staff = "line5" {
            \set Staff.instrumentName = \markup { Line5 }
            \set Staff.shortInstrumentName = \markup { Line5 }
            {
                \accidentalStyle modern-cautionary
                e'1
                f'1
            }
        }
    >>
}