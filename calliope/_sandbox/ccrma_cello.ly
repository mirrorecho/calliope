\version "2.12.2"

\language "english"

% LILYPOND NOTES:
% context settings vs grob overrides... difficult to know when one of the other
% context settings need to be set within context with \set
% look into lilypond & abjad tagging systems
% tag is kwarg to attach... use it!! (tag all attachments!)
% look at cross-segment example on glissando

% most algorythmic compositional systems ... model seriously questionsed?
% - e.g. don't have query interfaces
% - look at Jeff's dissertation



% #(set-default-paper-size "letter" 'landscape) % old code
#(set-default-paper-size "letterlandscape") % new code
#(set-global-staff-size 29)

\new Score \with {
    % remove \set in with block because with expects context settings
    % \set Score.proportionalNotationDuration = #(ly:make-moment 1 64)
    proportionalNotationDuration = #(ly:make-moment 1 64)
    \override SpacingSpanner.strict-grace-spacing = ##t
    \override SpacingSpanner.strict-note-spacing = ##t
    \override SpacingSpanner.uniform-stretching = ##t
}
<<
    % \set Score.proportionalNotationDuration = #(ly:make-moment 1 64)
    % \override Score.SpacingSpanner.strict-grace-spacing = ##t
    % \override Score.SpacingSpanner.strict-note-spacing = ##t
    % \override Score.SpacingSpanner.uniform-stretching = ##t
    \new PianoStaff 
    \with {
        \override StaffGrouper.staff-staff-spacing.minimum-distance = 18
    }
    <<
        % THIS IS MY RH STAFF
        \new Staff 
        \with {
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
            instrumentName = \markup { \hcenter-in #6 RH }
        }
        <<
            \new Voice 
            {
                \time 9/16
                s1 * 9/16
                \time 7/16
                s1 * 7/16
            }
            \new Voice 
            {
                b'8
                \f
                \<
                \glissando 
                b' 
                \glissando
                b'16 
                \glissando
                b'16 
                \glissando
                b'8
                [
                \glissando
                b'8
                \glissando
                b'16 
                \glissando
                b'16
                ]
                \glissando 
                \times 2/3 
                { 
                    b'4 
                    \ff
                    \>
                    \glissando
                    b'8 
                    \f
                }
            }
        >>
        % THIS IS MY LH STAFF
        \new Staff 
        \with {
            \override BarLine.transparent = ##t
            \override Glissando.thickness = 3
        }
        {
            \new Voice 
            {
                \times 2/3 
                { 
                    \clef bass
                    d'8 
                    \glissando                    

                    cs'1 
                    \glissando

                    ef'4 
                    \glissando 
                    d'8 
                }
            }
        }
    >>
>>

