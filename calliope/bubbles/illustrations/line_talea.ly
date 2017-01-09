% 2016-11-30 22:35

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \new Staff {
            \set Staff.instrumentName = \markup { LineTalea }
            \set Staff.shortInstrumentName = \markup { LineTalea }
            {
                \accidentalStyle modern-cautionary
                c'4
                r4
                c'4
                r4
            }
        }
    >>
}