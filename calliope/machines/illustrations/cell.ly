% 2018-07-27 01:04

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    {
        c'4
        b4
        c'4
        b4
        d'4
        ef'4
        {
            \times 4/5 {
                f4 ~
                g4 ~
                a4 ~
                b4 ~
                c'4
            }
        }
        c'4
        b4
        c'4
        b4
    }
}