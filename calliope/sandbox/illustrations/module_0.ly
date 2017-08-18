% 2017-08-18 01:16

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "Flute" {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Flute }
            {
                d'4
                d'4
                d'4
                d'4
            }
        }
        \context Staff = "Violin" {
            \set Staff.instrumentName = \markup { Violin }
            \set Staff.shortInstrumentName = \markup { Violin }
            {
                c'4
                c'4
                c'4
                c'4
            }
        }
    >>
}