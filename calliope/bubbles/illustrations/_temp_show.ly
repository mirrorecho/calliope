% 2017-08-12 23:37

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "my_line1_0" {
            \set Staff.instrumentName = \markup { My_line1_0 }
            \set Staff.shortInstrumentName = \markup { My_line1_0 }
            {
                {
                    \accidentalStyle modern-cautionary
                    e'4
                    g'8 [
                    fs'8 ]
                    e''4
                    b'4
                }
            }
        }
        \context Staff = "my_line1_1" {
            \set Staff.instrumentName = \markup { My_line1_1 }
            \set Staff.shortInstrumentName = \markup { My_line1_1 }
            {
                {
                    \accidentalStyle modern-cautionary
                    d''4
                    c''8 [
                    e'8 ]
                    g'4
                    bf'4
                }
            }
        }
        \context Staff = "my_line1_2" {
            \set Staff.instrumentName = \markup { My_line1_2 }
            \set Staff.shortInstrumentName = \markup { My_line1_2 }
            {
                {
                    \accidentalStyle modern-cautionary
                    f'4
                    f''8 [
                    e''8 ]
                    d''4
                    ef''4
                }
            }
        }
        \context Staff = "my_line1_3" {
            \set Staff.instrumentName = \markup { My_line1_3 }
            \set Staff.shortInstrumentName = \markup { My_line1_3 }
            {
                {
                    \accidentalStyle modern-cautionary
                    a'4
                    d''8 [
                    b'8 ]
                    a'4
                    af'4
                }
            }
        }
        \context Staff = "my_line1_4" {
            \set Staff.instrumentName = \markup { My_line1_4 }
            \set Staff.shortInstrumentName = \markup { My_line1_4 }
            {
                {
                    \accidentalStyle modern-cautionary
                    d'4
                    f'8 [
                    g'8 ]
                    g''4
                    af''4
                }
            }
        }
    >>
}