% 2017-08-10 11:32

\version "2.19.54"
\language "english"

\header {}

\layout {}

\paper {}

\score {
    \new Score <<
        \context Staff = "clusters_3" {
            \set Staff.instrumentName = \markup { Clusters_3 }
            \set Staff.shortInstrumentName = \markup { Clusters_3 }
            {
                \makeClusters <<
                    {
                    }
                    {
                    }
                >>
                \makeClusters <<
                    {
                    }
                    {
                    }
                >>
                \makeClusters <<
                    {
                    }
                    {
                    }
                >>
            }
        }
    >>
}