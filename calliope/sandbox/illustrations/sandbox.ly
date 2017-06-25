% 2017-06-23 23:34

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context StaffGroup = "Strings" <<
            \context StaffGroup = "Violins" \with {
                systemStartDelimiter = #'SystemStartSquare
            } <<
                \context Staff = "Violin1" {
                    \set Staff.instrumentName = \markup { "Violin 1" }
                    \set Staff.shortInstrumentName = \markup { Vln.1 }
                    {
                        \accidentalStyle modern-cautionary
                        b4
                        b4
                    }
                }
                \context Staff = "Violin2" {
                    \set Staff.instrumentName = \markup { "Violin 2" }
                    \set Staff.shortInstrumentName = \markup { Vln.2 }
                }
            >>
            \context Staff = "Viola" {
                \set Staff.instrumentName = \markup { Viola }
                \set Staff.shortInstrumentName = \markup { Vla. }
                {
                    \accidentalStyle modern-cautionary
                    a4
                    a4
                }
            }
            \context Staff = "Cello" {
                \clef "bass"
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
                {
                    \accidentalStyle modern-cautionary
                    c'2
                }
            }
        >>
    >>
}