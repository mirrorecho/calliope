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
        \context StaffGroup = "Violins"
        <<
            \context Staff = "Violin1Staff"
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                {
                    {
                        c'4
                        d'4
                        ef'4
                        f'4
                        ~
                        f'1
                    }
                }
            }
            \context Staff = "Violin2Staff"
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                {
                    c'1
                    b2
                    b2
                }
            }
        >>
    >>
}