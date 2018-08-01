% #(set-default-paper-size "letter" 'landscape) % old code
#(set-default-paper-size "letterlandscape") % new code
#(set-global-staff-size 29)


\layout 
{
    \context 
    {
        \Score
        proportionalNotationDuration = #(ly:make-moment 1 64)
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
    }
    \context 
    {
        \PianoStaff
        \accepts RHStaff
        \accepts LHStaff
        \override StaffGrouper.staff-staff-spacing.minimum-distance = 18
    }
    \context
    {
        \Staff
        \name RHStaff
        \type Engraver_group
        \alias Staff
        \override BarLine.bar-extent = #'(0 . 0)
        \override Beam.positions = #'(-6 . -6)
        \override Clef.stencil = ##f
        \override DynamicLineSpanner.staff-padding = 9
        \override Glissando.bound-details.left.padding = 0.25
        \override Glissando.bound-details.left.start-at-dot = ##f
        \override Glissando.bound-details. right.padding = 0
        \override Glissando.thickness = 6
        \override NoteHead.stencil = ##f
        \override StaffSymbol.line-positions = #'(0)
        \override Stem.length = 10
        instrumentName = \markup { \hcenter-in #6 RHYO }
    }
    \context
    {
        \Staff
        \name LHStaff
        \type Engraver_group
        \alias Staff
        \override BarLine.transparent = ##t
        \override Glissando.thickness = 3
        instrumentName = \markup { \hcenter-in #6 LH }
    }
}