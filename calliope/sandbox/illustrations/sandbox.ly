% 2018-07-22 13:47

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \time 3/4
    {
        \numericTimeSignature
        \accidentalStyle modern-cautionary
        \numericTimeSignature
        c'4 ^ \markup { "time 3/4" }
        c'8 [
        c'8 ~ ]
        c'2 ~
        c'8 [
        c'8 ~ ]
        c'4 ~
        c'2 ~
        c'8 [
        c'8 ~ ]
        c'4 ~
        c'4 ~
        c'8 [
        c'8 ]
        c'8 [
        c'8 ~ ]
        c'4 ~
        c'2 ~
        c'8 [
        c'8 ~ ]
        c'16 [
        c'8. ~ ]
        c'2 ~
        c'1 ~
        c'4
        c'4 ~
        c'2
        c'1 ~
        c'1 ~
        c'4
        c'8 [
        c'8 ]
        c'2
    }
}