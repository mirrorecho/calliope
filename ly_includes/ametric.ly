
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DASHED STAFF LINES: see:
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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% little brackets/lines before/after the ametric music:

% The number next to "th" in (th 0.2) controls thickness of the brackets. 
#(define-markup-command (left-bracket layout props) ()
"Draw left hand bracket"
  (let* ((th .08);;todo: take from GROB
          (width (* 4 th)) ;; todo: take from GROB
          (ext '(-4.9 . 4))) ;; todo: take line-count into account
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
          (width (* 2 th)) ;; todo: take from GROB
          (ext '(-1.4 . 1.4))) ;; todo: take line-count into account
        (ly:bracket Y ext th (- width))))

rightBracket = {
    {
    \once\override BreathingSign.text = #(make-right-bracket-markup)
    \once\override BreathingSign.Y-offset = ##f
    \breathe
    }
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

freeOn = {
    \hideNotes
        \stopStaff
      % \override Staff.StaffSymbol #'line-positions = #'( -4 -2 -0.1 0 0.1 2 4 )
      % \dashedStaffSymbolLines #'( #t #t #f #f #f #t #t )
      \override Staff.StaffSymbol #'line-positions = #'( -4 4 )
      \dashedStaffSymbolLines #'( #t #t )
        \startStaff
    \grace {
    
    % \override Score.SpacingSpanner.spacing-increment = #20


        % b1

        % \leftBracket

        % \revert Score.SpacingSpanner.spacing-increment



    }

\draw-line #'(5.1 . 2.3)
  \override #'(on . 0.3)
  \override #'(off . 0.5)
  \draw-dashed-line #'(5.1 . 2.3)

        \stopStaff
        \dashedStaffSymbolLines #'( #f #f #f #f #f )
        \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
    \unHideNotes  

}

freeAfter = {
    \hideNotes
    \grace {
        r16  
        \stopStaff
        \override Staff.StaffSymbol #'line-positions = #'( -4 -2  0 2 4 )
        \dashedStaffSymbolLines #'( #t #t #t #t #t  )
        % \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
        r8
    }
}

freeLine = {
    % \rightBracket
    \hideNotes
    \grace {
        r16  
        \stopStaff
        \override Staff.StaffSymbol #'line-positions = #'( -4 -2 -0.1 0 0.1 2 4 )
        \dashedStaffSymbolLines #'( #t #t #f #f #f #t #t )
        % \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
        r16  
    }
}

freeLineArrow = {
      \unHideNotes
      \grace {
        \once \override Rest  #'stencil = #ly:text-interface::print
        \once \override Rest.staff-position = #-1.4
        \once \override Rest #'text = \markup { \fontsize #3 { \general-align #Y #DOWN { \arrow-head #X #RIGHT ##t } } }
        r8
      }
      \hideNotes
}


% freeLineArrow = {
%     {
%         \once \override BreathingSign  #'stencil = #ly:text-interface::print
%         \once\override BreathingSign.Y-offset = #-0.68
%         \once\override BreathingSign.X-offset = #-2
%         \once \override BreathingSign #'text = \markup { \fontsize #3 { \general-align #Y #DOWN { \arrow-head #X #RIGHT ##t } } }
%     \breathe
%     }
% }


freeOff = {
    \grace {
        \stopStaff
        \dashedStaffSymbolLines #'( #f #f #f #f #f )
        \override Staff.StaffSymbol #'line-positions = #'()
        \startStaff
    }
    \unHideNotes  
}

timeX = {
    \once \override 
    Staff.TimeSignature #'stencil = #(lambda (grob)
    (parenthesize-stencil (grob-interpret-markup grob 
    (markup #:override '(baseline-skip . 0.5) #:column ("X" "X"))
    ) 0.1 0.4 0.4 0.1 ))
}