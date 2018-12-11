\version "2.19.82"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    \context Staff = "MyStaffB"
    \with
    {
        \consists Horizontal_bracket_engraver
    }
    {
        {
            r2
            r4
            d'4
            ~
            d'2
            e'2
        }
        {
            fs'2
            d'2
            e'1
            -\accent
        }
    }
}