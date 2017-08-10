% 2017-08-09 22:40

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "Flute" {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
        }
        \context Staff = "Clarinet" {
            \set Staff.instrumentName = \markup { "Clarinet in Bb" }
            \set Staff.shortInstrumentName = \markup { Cl. }
        }
        \context StaffGroup = "MyStaffGroup" <<
            \context Staff = "Violin1" {
                \set Staff.instrumentName = \markup { "Violin 1" }
                \set Staff.shortInstrumentName = \markup { Vln. }
                {
                    \accidentalStyle modern-cautionary
                    <<
                    >>
                    <<
                    >>
                }
            }
            \context Staff = "Violin2" {
                \set Staff.instrumentName = \markup { "Violin 2" }
                \set Staff.shortInstrumentName = \markup { Vln. }
                {
                    \accidentalStyle modern-cautionary
                    <<
                    >>
                    <<
                    >>
                }
            }
        >>
    >>
}