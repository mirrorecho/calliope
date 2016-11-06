% 2016-11-03 15:15

\version "2.18.2"
\language "english"

\header {
    tagline = ##f
}

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
        \new Staff {
            \set Staff.instrumentName = \markup { YoMama }
            \set Staff.shortInstrumentName = \markup { YoMama }
            {
                {
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { YoMama1 }
            \set Staff.shortInstrumentName = \markup { YoMama1 }
            {
                {
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { YoMama2 }
            \set Staff.shortInstrumentName = \markup { YoMama2 }
            {
                {
                }
            }
        }
        \new Staff {
            \set Staff.instrumentName = \markup { C }
            \set Staff.shortInstrumentName = \markup { C }
            {
                {
                    \accidentalStyle modern-cautionary
                    c1
                }
            }
        }
    >>
}