\version "2.19.82"

\language "english"



{

    \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
    \set tupletFullLength = ##t
    \times 2/3 
    { 
        c'4
    }
    \times 2/3 
    { 
        c'4
    }
    \times 2/3 
    { 
        c'4
    }
    \times 2/3 
    { 
        c'4
    }
    \times 2/3 
    { 
        c'4
    }
    \times 2/3 
    { 
        c'4
    }
}

% {
%     \override TupletBracket.color = #red
%     \times 2/3 {

%         \times 2/3 {
%             \ottava #1
%             b4 
%             -\tweak color #blue % must start with - to make it applly to post event
%             ^ (
%             \tweak Accidental.color #blue
%             \tweak Stem.color #blue
%             \tweak color #blue
%             bs4
%             b4
%         }
%         a2
%         \ottava #0
%         a2
%         )
%     }
% }
