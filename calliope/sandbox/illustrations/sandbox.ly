% 2017-06-22 12:49

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "m1" {
            \set Staff.instrumentName = \markup { M1 }
            \set Staff.shortInstrumentName = \markup { M1 }
        }
        \context Staff = "m2" {
            \set Staff.instrumentName = \markup { M2 }
            \set Staff.shortInstrumentName = \markup { M2 }
        }
    >>
}