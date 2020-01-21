\version "2.19.82"
\language "english"

\header {
    tagline = ##f
    composer = \markup { "Randall West" }
}

\layout {}

\paper {}

\score {
    \new Score
    <<
        \new RhythmicStaff
        \with
        {
            \consists Horizontal_bracket_engraver
        }
        {
            {
                \numericTimeSignature
                \accidentalStyle neo-modern-cautionary
                \time 8/4
                \clef "percussion"
                s4
                c'2
                c'2
                s4
            }
        }
    >>
}