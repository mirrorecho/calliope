% 2017-03-22 00:48

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \new Staff {
            \set Staff.instrumentName = \markup { BaseLine0 }
            \set Staff.shortInstrumentName = \markup { BaseLine0 }
            {
                {
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { Violin1 }
            \set Staff.shortInstrumentName = \markup { Violin1 }
            {
                {
                    \accidentalStyle modern-cautionary
                    d'2
                    e'2
                }
                {
                    \accidentalStyle modern-cautionary
                    d2
                    d2
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { Violin2 }
            \set Staff.shortInstrumentName = \markup { Violin2 }
            {
                {
                    \accidentalStyle modern-cautionary
                    c1
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { Viola }
            \set Staff.shortInstrumentName = \markup { Viola }
            {
                {
                    \accidentalStyle modern-cautionary
                    c1
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { Cello }
            \set Staff.shortInstrumentName = \markup { Cello }
            {
                {
                    \accidentalStyle modern-cautionary
                    c1
                }
            }
        }
    >>
}