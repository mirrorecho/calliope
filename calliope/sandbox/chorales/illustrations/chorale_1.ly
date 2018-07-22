% 2018-07-15 14:59

\version "2.18.2"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "Soprano" \with {
            \consists Horizontal_bracket_engraver
        } {
            \set Staff.instrumentName = \markup { Soprano }
            \set Staff.shortInstrumentName = \markup { Soprano }
            {
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
                {
                    b'8 [
                    c''8 ]
                    b'8 [
                    a'8 ]
                    e''8 [
                    e''16
                    d''16 ]
                    c''8 [
                    b'8 ~ ]
                    b'8 [
                    r8 ]
                }
            }
        }
        \context Staff = "Alto" \with {
            \consists Horizontal_bracket_engraver
        } {
            \set Staff.instrumentName = \markup { Alto }
            \set Staff.shortInstrumentName = \markup { Alto }
            {
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
                {
                    gs'8 [
                    a'8 ]
                    gs'8 [
                    a'8 ]
                    gs'16 [
                    a'16
                    b'8 ]
                    e'16 [
                    fs'16
                    gs'8 ~ ]
                    gs'8 [
                    r8 ]
                }
            }
        }
        \context Staff = "Tenor" \with {
            \consists Horizontal_bracket_engraver
        } {
            \set Staff.instrumentName = \markup { Tenor }
            \set Staff.shortInstrumentName = \markup { Tenor }
            {
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e'8 [
                    e'8 ]
                    d'8 [
                    e'8 ]
                    d'16 [
                    c'16
                    b8 ]
                    c'16 [
                    d'16
                    e'8 ~ ]
                    e'8 [
                    r8 ]
                }
            }
        }
        \context Staff = "Bass" \with {
            \consists Horizontal_bracket_engraver
        } {
            \set Staff.instrumentName = \markup { Bass }
            \set Staff.shortInstrumentName = \markup { Bass }
            {
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
                {
                    \clef "bass"
                    e8 [
                    a8 ]
                    b8 [
                    c'8 ]
                    b16 [
                    a16
                    gs8 ]
                    a8 [
                    e8 ~ ]
                    e8 [
                    r8 ]
                }
            }
        }
    >>
}