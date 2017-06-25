% 2017-06-25 00:30

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "phrase1" {
            \set Staff.instrumentName = \markup { Phrase1 }
            \set Staff.shortInstrumentName = \markup { Phrase1 }
            {
                \accidentalStyle modern-cautionary
                bf2
                af4
                g4
                ef'2
                e'2
            }
        }
    >>
}