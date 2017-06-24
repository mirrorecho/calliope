% 2017-06-23 13:22

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "MyLine2" {
            \set Staff.instrumentName = \markup { MyLine2 }
            \set Staff.shortInstrumentName = \markup { MyLine2 }
            {
                \accidentalStyle modern-cautionary
                b4
                b4
            }
        }
        \context Staff = "MyLine1" {
            \set Staff.instrumentName = \markup { MyLine1 }
            \set Staff.shortInstrumentName = \markup { MyLine1 }
            {
                \accidentalStyle modern-cautionary
                a4
                a4
            }
        }
        \context Staff = "LINE3" {
            \set Staff.instrumentName = \markup { LINE3 }
            \set Staff.shortInstrumentName = \markup { LINE3 }
            {
                \accidentalStyle modern-cautionary
                b4
                b4
            }
        }
    >>
}