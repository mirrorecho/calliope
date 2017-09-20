% 2017-09-19 23:11

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    <<
        {
            {
                \accidentalStyle modern-cautionary
                r8
                c'4. \startGroup
                c'2 ~
                c'8
                c'4
                c'4.
                c'4 ~
                c'4.
                c'8 \stopGroup [
                r8 ]
                c'4. \startGroup
                c'2.
                c'4 ~
                c'4.
                c'8 \stopGroup [
                r2 ]
            }
        }
        {
            {
                \accidentalStyle modern-cautionary
                r2 [
                c'8
                c'8 ]
                c'4
                c'4
                c'8 [
                c'8
                c'8
                c'8 ]
                c'4
                c'4
                c'8 [
                c'8
                c'8
                c'8 ]
                c'4
                c'4
                c'4
                c'4
                c'8 [
                c'8 ]
            }
        }
    >>
}