% 2017-11-16 23:23

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    {
        d'4
        e'4
        f'8 -\accent -\staccato [
        g'8 ]
        d'4 -\accent ~
        d'4
        e'2 -\accent -\staccato
        f'16 -\accent -\staccato [
        g'16 -\accent
        a'8 -\accent ]
        d'4 -\accent
        r4
        f'4 -\accent -\staccato
        r4
        a'4
        r2.
    }
}