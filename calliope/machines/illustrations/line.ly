\version "2.19.82"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    <<
        {
            {
                \accidentalStyle modern-cautionary
                c'4
                c''4
                ~
                c''4
            }
        }
        {
            {
                \accidentalStyle modern-cautionary
                d'2
                g'4
            }
        }
    >>
}