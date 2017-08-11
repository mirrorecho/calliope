% 2017-08-10 12:15

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "clusters_I" {
            \set Staff.instrumentName = \markup { Clusters_I }
            \set Staff.shortInstrumentName = \markup { Clusters_I }
            {
                \makeClusters {
                    \override NoteHead.color = #red
                    c,,4
                    a''''4
                    b'4
                    \revert NoteHead.color
                }
                \makeClusters {
                    \override NoteHead.color = #red
                    c,,4
                    a''''4
                    b'4
                    \revert NoteHead.color
                }
                \makeClusters {
                    \override NoteHead.color = #red
                    c,,4
                    a''''4
                    b'4
                    \revert NoteHead.color
                }
            }
        }
    >>
}