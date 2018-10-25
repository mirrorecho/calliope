\version "2.12.2"

\language "english"
\include "ccrma-cello-stylesheet.ily"

% LILYPOND NOTES:
% context settings vs grob overrides... difficult to know when one of the other
% context settings need to be set within context with \set
% look into lilypond & abjad tagging systems
% tag is kwarg to attach... use it!! (tag all attachments!)
% look at cross-segment example on glissando

% most algorythmic compositional systems ... model seriously questionsed?
% - e.g. don't have query interfaces
% - look at Jeff's dissertation





\new Score \with {
    % remove \set in with block because with expects context settings
    % \set Score.proportionalNotationDuration = #(ly:make-moment 1 64)
}
<<
    % \set Score.proportionalNotationDuration = #(ly:make-moment 1 64)
    % \override Score.SpacingSpanner.strict-grace-spacing = ##t
    % \override Score.SpacingSpanner.strict-note-spacing = ##t
    % \override Score.SpacingSpanner.uniform-stretching = ##t
    \new PianoStaff 
    <<
        % THIS IS MY RH STAFF
        \new RHStaff 
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
        \new LHStaff 
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

