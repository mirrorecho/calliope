%%%%%%%%%%%%%%%%%% 
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


% free time (everyone fully noted)  ... SHOWING TIME SPANS
% free time some systems
% free time everyone systems


% metered time (everyone)
% metered time (some systems)




\score {
\new Score <<

    {
        \override ParenthesesItem.font-size = #6.9
        \startParenthesis \parenthesize
        f8
        g'''
        c'
        b'
        b1
        f8
        c'
        b'
        \endParenthesis \parenthesize
        g'''
        b1
        a1
    }


    {
        g1
        g'^\markup { \translate #'(-1 . -7) { "(" } } 
        g
    }


>>
}