% 2017-12-30 10:42

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new TabStaff {
        \set Staff.stringTunings = \stringTuning <c' g' d''>
        {
            c'8 g''8
        }
      }
}