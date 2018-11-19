\version "2.19.82"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    \new Staff
    \with
    {
        \consists Horizontal_bracket_engraver
    }
    {
        {
            a2
            a2
            d'1
        }
        {
            d'1
            a2
            a2
        }
    }
}