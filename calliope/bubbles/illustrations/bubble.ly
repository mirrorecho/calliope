% 2017-08-17 22:40

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
            {
                d'4
                d'4
                d'4
                d'4
            }
            {
                d''4
                d''4
                d''4
                d''4
            }
        }
        \context Staff = "Clarinet" {
            \set Staff.instrumentName = \markup { "Clarinet in Bb" }
            \set Staff.shortInstrumentName = \markup { Cl. }
        }
        \context StaffGroup = "StringsStaffGroup" <<
            \context Staff = "Violin" {
                \set Staff.instrumentName = \markup { Violin }
                \set Staff.shortInstrumentName = \markup { Vln. }
                {
                    c'4
                    c'4
                    c'4
                    c'4
                }
                {
                    c''4
                    c'''4
                    c''4
                    c''4
                }
            }
            \context Staff = "Cello" {
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
                {
                    \clef "bass"
                    c1
                }
            }
        >>
    >>
}