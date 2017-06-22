% 2017-06-22 00:58

\version "2.19.54"
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
    >>
}