% 2018-07-27 00:02

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    {
        \numericTimeSignature
        \time 4/4
        \partial 4
        r4 ^ \markup { YO }
        c'8 [ ^ \markup { YO }
        c'8 ~ ]
        c'4 ~
        c'4 ~
        c'8 [
        r8 ] ^ \markup { YO }
        r2
        r4
        r8 [
        c'8 ~ ] ^ \markup { YO }
        c'2 ~
        c'8 [
        c'8 ]
        c'8 [
        c'8 ~ ]
        c'2 ~
        c'4 ~
        c'8 [
        c'8 ~ ]
        c'16 [
        c'8. ~ ]
        c'4 ~
        c'2 ~
        c'1
        c'2 ~
        c'4
        c'4 ~
        c'1 ~
        c'1
        c'8 [
        c'8 ]
        c'4 ~
        c'4
    }
}