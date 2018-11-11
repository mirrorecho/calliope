\version "2.19.82"
\language "english"

\include "../../stylesheets/score.ily"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    \new Score
    <<
        \context Staff = "Violin"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                e'2
                ~
                e'4
                g'4
                ~
                g'2
                f'2
                ~
                f'4
                ef'4
                ~
                ef'2
                c'2
                d'2
                ~
                d'2
                c'2
                ~
                c'2
                d'2
            }
        }
        \context Staff = "Cello"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                \clef "bass"
                e'2
                g'2
                f'2
                ef'2
                c'2
                d'2
                c'2
                d'2
            }
        }
    >>
}