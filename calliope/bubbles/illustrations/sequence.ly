% 2017-08-17 00:21

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    <<
        {
            {
                d'4
                d'4
                d'4
                d'4
            }
            {
                \clef "bass"
                d,4
                d,4
                d,4
                d,4
            }
        }
        {
            {
                c'4
                c'4
                c'4
                c'4
            }
            {
                \clef "bass"
                c,4
                c,4
                c,4
                c,4
            }
        }
        {
            {
                a1
                b1
                c'2
                d'2
            }
            {
                \clef "bass"
                a1
                b1
                c,2
                d,2
            }
        }
        {
            {
                b'1
                c''1
                c''2
                d''2
            }
            {
                \clef "bass"
                b,1
                c,,1
                c,,2
                d,,2
            }
        }
    >>
}