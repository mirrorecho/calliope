\version "2.19.82"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    \new Score
    <<
        \context Staff = "violin1"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                e'4
                c'4
                r4
                g'4
                r2
                r4
                fs'4
                ~
                fs'4
            }
        }
        \context Staff = "violin2"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                d'4
                c'4
                r4
                g'4
                r2
                r4
                fs'4
                ~
                fs'4
            }
        }
    >>
}