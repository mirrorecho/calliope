% musicOne = \relative {
%   c''4 b8. a16 g4. f8 e4 d c2
% }

% \score {
%   <<
%     {
      
%       {
%             {
%               \time 2/4
%               \musicOne
%             }
%             {
%               \musicOne
%             }
%       }
%       \addlyrics {
%           Happiness to the everyone, here we all are. Happiness to the everyone, here we all are.
%       }    

%     }
%   >>
% }

\version "2.18.2"
\language "english"


%%http://lsr.di.unimi.it/LSR/Item?id=880

% original code (for zig-zag lines) by Thomas Morley (Harm)
% -> http://lists.gnu.org/archive/html/lilypond-user/2012-12/msg00715.html
% slightly modified to create dashed lines by Paul Morris

dashedStaffSymbolLines =
#(define-music-function (parser location dash-space bool-list)
 ((number-pair? '(0.02 . 0.4)) list?)
"
Replaces specified lines of a StaffSymbol with dashed lines.

The lines to be changed should be given as a list containing booleans, with
the meaning:
  #f - no dashes, print a normal line
  #t - print a dashed line
The order of the bool-list corresponds with the order of the given list of
'line-positions or if not specified, with the default.
If the length of the bool-list and the 'line-positions doesn't match a warning
is printed.

The width of the dashes and the spacing between them can be altered by adding a pair
as first argument while calling the function:
\\dashedStaffSymbolLines #'(1 . 1) #'(#f #f #t #f #f)
the first number of the pair is the width, the second the spacing
"
#{
 \override Staff.StaffSymbol.after-line-breaking =
   #(lambda (grob)
     (let* ((staff-stencil (ly:grob-property grob 'stencil))
            (staff-line-positions 
              (if (equal? (ly:grob-property grob 'line-positions) '() )
                '(-4 -2 0 2 4)
                (ly:grob-property grob 'line-positions)))
            (staff-width
              (interval-length
                (ly:stencil-extent staff-stencil X)))
            (staff-space (ly:staff-symbol-staff-space grob))
            (staff-line-thickness (ly:staff-symbol-line-thickness grob))
            ;; width of the dash
            (dash-width (car dash-space))
            ;; space between dashes
            (space-width (cdr dash-space))
            ;; Construct the first dash
            (sample-path `((moveto 0 0)
                           (lineto ,dash-width 0)
                           ))
            ;; Make a stencil of the first dash
            (dash-stencil
              (grob-interpret-markup
                grob
                (markup
                  #:path staff-line-thickness sample-path)))
           ;; width of both dash and space
           (dash-space-width (+ dash-width space-width))
           
           ;; another way: get width of dash from the dash stencil
           ;; (stil-width
           ;;   (interval-length
           ;;     (ly:stencil-extent dash-stencil X)))
           ;; (dash-space-width (+ stil-width space-width))
           
            ;; Make a guess how many dashes are needed.
            (count-dashes
              (inexact->exact
                (round
                  (/ staff-width
                     (- dash-space-width
                        staff-line-thickness)))))
            ;; Construct a stencil of dashes with the guessed count
            (dashed-stil
                (ly:stencil-aligned-to
                  (apply ly:stencil-add
                    (map
                      (lambda (x)
                        (ly:stencil-translate-axis
                          dash-stencil
                          (* (- dash-space-width staff-line-thickness) x)
                          X))
                      (iota count-dashes)))
                  Y
                  CENTER))
            ;; Get the the length of that dashed stencil
            (stil-x-length
              (interval-length
                (ly:stencil-extent dashed-stil  X)))
            ;; Construct a line-stencil to replace the staff-lines.
            (line-stil
              (make-line-stencil staff-line-thickness 0 0 staff-width 0))
            ;; Calculate the factor to scale the dashed-stil to fit
            ;; the width of the original staff-symbol-stencil
            (corr-factor
              (/ staff-width (- stil-x-length staff-line-thickness)))
            ;; Construct the new staff-symbol
            (new-stil
              (apply
                ly:stencil-add
                  (map
                    (lambda (x y)
                      (ly:stencil-translate
                          (if (eq? y #f)
                            line-stil
                            (ly:stencil-scale
                              dashed-stil
                              corr-factor 1))
                          (cons (/ staff-line-thickness 2)
                                (* (/ x 2) staff-space))))
                    staff-line-positions bool-list))))
       
      (if (= (length bool-list)(length staff-line-positions))
        (ly:grob-set-property! grob 'stencil new-stil)
        (ly:warning
          "length of dashed line bool-list doesn't match the line-positions - ignoring"))))
#})


startParenthesis = {
  \once \override ParenthesesItem.stencils = #(lambda (grob)
        (let ((par-list (parentheses-item::calc-parenthesis-stencils grob)))
          (list (car par-list) point-stencil )))
}

endParenthesis = {
  \once \override ParenthesesItem.stencils = #(lambda (grob)
        (let ((par-list (parentheses-item::calc-parenthesis-stencils grob)))
          (list point-stencil (cadr par-list))))
} 

endBarCurlyPath = \markup {
    \with-dimensions #'(0 . 0) #'(0 . 0)
    \override #'(filled . #t) 
    \path #0.01 
    #'((moveto   -0.01   -0.95)
       (curveto   0.05   -1.10   0.02  -1.50   0.12   0.00)
       (curveto   0.18    0.80   0.25   1.63   0.38   1.63)
       (curveto   0.51    1.63   0.52   0.80   0.59   0.00)
       (curveto   0.66   -0.90   0.70  -1.54   0.91  -1.54)
       (curveto   1.04   -1.54   1.08  -1.10   1.23   0.00)
       (curveto   1.35    1.00   1.46   1.00   1.49   1.00)
       (curveto   1.57    1.00   1.59   0.69   1.63   0.00)
       (curveto   1.68   -0.70   1.75  -1.08   1.90  -1.08)
       (curveto   2.05   -1.08   2.05  -0.80   2.12  -0.30)
       (curveto   2.20    0.20   2.22   0.43   2.30   0.43)
       (curveto   2.36    0.43   2.37   0.20   2.43   0.00)
       (curveto   2.49   -0.20   2.51  -0.33   2.76  -0.34)
       (curveto   2.96   -0.34   3.20  -0.20   3.25  -0.07)
       (curveto   3.27   -0.01   3.24   0.00   3.23   0.00)
       (curveto   3.15    0.00   3.05  -0.30   2.80  -0.31)
       (curveto   2.67   -0.31   2.64  -0.27   2.55   0.05)
       (curveto   2.46    0.40   2.50   0.48   2.30   0.48)
       (curveto   2.15    0.48   2.10   0.00   2.07  -0.25)
       (curveto   2.00   -0.70   1.98  -1.02   1.92  -1.02)
       (curveto   1.82   -1.02   1.83  -0.60   1.80   0.05)
       (curveto   1.78    0.55   1.74   1.04   1.50   1.04)
       (curveto   1.30    1.04   1.25   0.65   1.16   0.00)
       (curveto   1.02   -1.20   0.96  -1.48   0.91  -1.48)
       (curveto   0.82   -1.48   0.82  -0.70   0.80  -0.25)
       (curveto   0.71    0.90   0.68   1.68   0.40   1.68)
       (curveto   0.15    1.68   0.12   1.00  -0.01  -0.40)
       (closepath))
    }
    
endBarCurly = {
  \once \override  BreathingSign.stencil =
  #(lambda (grob)
     (ly:stencil-combine-at-edge
      (ly:bar-line::print grob)
      X RIGHT
      (grob-interpret-markup grob endBarCurlyPath)
      0))
  \breathe
}


%here starts the snippet:

% The number next to "th" in (th 0.2) controls thickness of the brackets. 
#(define-markup-command (left-bracket layout props) ()
"Draw left hand bracket"
(let* ((th 0.09) ;; todo: take from GROB
  (width (* 0 th)) ;; todo: take from GROB
  (ext '(-0.66 . 0.66))) ;; todo: take line-count into account
  (ly:bracket Y ext th width)))

leftBracket = {
  \once\override BreathingSign.text = #(make-left-bracket-markup)
  \once\override BreathingSign.break-visibility = #end-of-line-invisible
  \once\override BreathingSign.Y-offset = ##f
  % Trick to print it after barlines and signatures:
  \once\override BreathingSign.break-align-symbol = #'custos
  \breathe 
}


#(define-markup-command (right-bracket layout props) ()
"Draw right hand bracket"
  (let* ((th .09);;todo: take from GROB
          (width (* 0 th)) ;; todo: take from GROB
          (ext '(-0.66 . 0.66))) ;; todo: take line-count into account
        (ly:bracket Y ext th (- width))))

rightBracket = {
  \once\override BreathingSign.text = #(make-right-bracket-markup)
  \once\override BreathingSign.Y-offset = ##f
  \breathe
}


beforeFree = {
      \hideNotes
      \grace {
        \stopStaff
        % \override Staff.StaffSymbol #'line-positions = #'( -4 -2  0 2 4 )
        % \dashedStaffSymbolLines #'( #t #t #t #t #t )
      \override Staff.StaffSymbol #'line-positions = #'( -4 -2 0 2 4 )
      \dashedStaffSymbolLines #'( #t #t #t #t #t )
        \startStaff
        s16
        \stopStaff
        \dashedStaffSymbolLines #'( #f #f #f #f #f )
        \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
      }
      \unHideNotes  
}

afterFreeOnly = {
      \hideNotes
      \stopStaff
      \override Staff.StaffSymbol #'line-positions = #'( -4 -2  0 2 4 )
      \dashedStaffSymbolLines #'( #t #t #t #t #t  )
      % \override Staff.StaffSymbol #'line-positions = #'()
      \startStaff
      \grace {
        r16 
      }
}

afterFree = {
      \hideNotes
      \stopStaff
      \override Staff.StaffSymbol #'line-positions = #'( -4 -2 -0.1 0 0.1 2 4 )
      \dashedStaffSymbolLines #'( #t #t #f #f #f #t #t )
      % \override Staff.StaffSymbol #'line-positions = #'()
      \startStaff
      \grace {
        r16  
      }
}

afterFreeContinue = {
      r4 %^"repeat 2 or  3 times"
      \unHideNotes
      \grace {
        \once \override Rest  #'stencil = #ly:text-interface::print
        \once \override Rest.staff-position = #-1.4
        \once \override Rest #'text = \markup { \fontsize #3 { \general-align #Y #DOWN { \arrow-head #X #RIGHT ##t } } }
        r16 
      }
      \hideNotes
      r2.
}

endFree = {
    \grace {
        \stopStaff
        \dashedStaffSymbolLines #'( #f #f #f #f #f )
        \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
        r32
    }
    \unHideNotes  
}

{

  \numericTimeSignature

            \once \override 
            Staff.TimeSignature #'stencil = #(lambda (grob)
            (parenthesize-stencil (grob-interpret-markup grob 
            (markup #:override '(baseline-skip . 0.5) #:column ("X" "X"))
            ) 0.1 0.4 0.4 0.1 ))
            \time 4/4

            {

              % \beforeFree
            c'1 a'2 b'2 
            % s4

          \beforeFree
          \leftBracket
              <> ^"freely, repeat 3 or 4 times"
              c''8  \pp b' a' g' ~ g'4. -\fermata 
          \rightBracket
              % \afterFreeOnly
              \afterFree
              r8
              % r8 ^"repeat 2 or 3 times"
              \afterFreeContinue
              \afterFreeContinue
              \afterFreeContinue
              \endFree
              % \time 4/4
              a4 ^"in time"
              g4 a2

            }
          }