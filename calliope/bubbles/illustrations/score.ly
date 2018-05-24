% 2018-02-19 11:00

\version "2.19.54"
\language "english"

\include "../../stylesheets/score.ily"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context RhythmicStaff = "STRAIGHT" \with {
            \consists Horizontal_bracket_engraver
        } {
            \clef "percussion"
            {
                c1
                c1
            }
        }
        \context RhythmicStaff = "SIMPLE" \with {
            \consists Horizontal_bracket_engraver
        } {
            \clef "percussion"
            {
                c1
                c1
            }
        }
    >>
}