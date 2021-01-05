\version "2.19.82"  %! abjad.LilyPondFile._get_format_pieces()
\language "english" %! abjad.LilyPondFile._get_format_pieces()

\header { %! abjad.LilyPondFile._get_formatted_blocks()
    tagline = ##f
    composer = \markup { "Randall West" }
} %! abjad.LilyPondFile._get_formatted_blocks()

\layout {}

\paper {}

\score { %! abjad.LilyPondFile._get_formatted_blocks()
    {
        r8
        [
        d'8
        ]
        e'8
        [
        f'8
        ]
        r2
    }
} %! abjad.LilyPondFile._get_formatted_blocks()