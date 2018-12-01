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
        \context Staff = "MyStaffA"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                c'2
                ~
                c'4
                d'4
                ~
                d'2
                e'2
            }
        }
        \context Staff = "MyStaffB"
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                c'2
                ~
                c'4
                d'4
                ~
                d'2
                e'2
            }
            {
                f'2
                e'2
            }
        }
    >>
}