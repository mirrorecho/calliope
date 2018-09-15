% 2018-07-11 23:23

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "TestLine" \with {
            \consists Horizontal_bracket_engraver
        } {
            \set Staff.instrumentName = \markup { TestLine }
            \set Staff.shortInstrumentName = \markup { TestLine }
            {
                \accidentalStyle modern-cautionary
                c'4
                d'4
                ef'4
                e'4
                a'4
                b4
                b'4
                fs'4
                af'4
                a'4
                e'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
            }
        }
    >>
}