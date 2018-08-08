\version "2.19.82"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    {
        {
            \numericTimeSignature
            \time 3/4
            \clef "bass"
            e'2.
            R2.
        }
        {
            \bar "!"
            cs'2.
            d'2
            r4
            b2.
        }
    }
}