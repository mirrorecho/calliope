% 2017-02-16 21:40

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \new StaffGroup <<
            \new StaffGroup \with {
                systemStartDelimiter = #'SystemStartSquare
            } <<
                \new Staff {
                    \set Staff.instrumentName = \markup { "Violin 1" }
                    \set Staff.shortInstrumentName = \markup { Vln.1 }
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
                    \set Staff.instrumentName = \markup { "Violin 2" }
                    \set Staff.shortInstrumentName = \markup { Vln.2 }
                    {
                        {
                            \accidentalStyle modern-cautionary
                            c1
                        }
                    }
                }
            >>
            \new Staff {
                \set Staff.instrumentName = \markup { Viola }
                \set Staff.shortInstrumentName = \markup { Vla. }
                {
                    {
                        \accidentalStyle modern-cautionary
                        c1
                    }
                }
            }
            \new Staff {
                \clef "bass"
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
                {
                    {
                        \accidentalStyle modern-cautionary
                        c1
                    }
                }
            }
        >>
        \new StaffGroup <<
        >>
        \new StaffGroup <<
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
        >>
    >>
}