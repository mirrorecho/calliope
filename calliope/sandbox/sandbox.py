import abjad, calliope
# # from calliope.sandbox import module_0, module_a


# class CellA(calliope.Cell):
#     set_rhythm =  (1, 1, 0.5, 0.5)
#     set_pitches = (2, 4, 5,   7)
# class CellB(calliope.Cell):
#     set_rhythm =  (2, 2, 0.25, 0.25, 0.5)
#     set_pitches = (2, 4, 5,    7,    9)
# class CellC(calliope.Cell):
#     set_rhythm =  (1, -1, 1, -1, 1)
#     set_pitches = (2, None, 5, None, 9)
# class CellD(CellC):
#     set_pitches = (1, None, 1, None, 1)

# class PhraseI(calliope.Phrase):
#     # cell_a = CellA
#     cell_b = CellB
#     cell_c = CellC
#     cell_c1 = CellC
#     cell_d = CellD

#     meter = (5,4)
#     # metrical_durations = ( (1,4), ((1,16),)*4, (2,4), (1,4) )
#     metrical_offset = -1

# pb = calliope.PhraseBlock(
#     PhraseI("yo1"), 
#     PhraseI("yo2", metrical_offset=0)
#     )

# p = PhraseI()

# for l in p.leaves:
#     print(l)

# p.cells[0,1].non_rest_events.tag(".", ">")
# p.events[2,3].non_rest_events.untag(">")

# p.non_rest_events[1].pitch = 22

# TO DO: why do the below behave differently?... should address:
# calliope.illustrate_me(bubble=pb)
# pb.illustrate_me()

# print(dir(m.root_node))

# RESTS MUST ONLY TAKE UP ONE NODE
# LOGICAL TIE NOTES MUST CAN TAKE UP MULTIPLE... BUT ONLY AT SAME LEVEL WITH SAME PARENT
# BEAMS SPECIFY LEVEL
m = abjad.Meter('''(4/4 (
        (2/4 (
            1/4
            1/4
            )
        )
        (2/4 (
            1/4
            1/4
            )
        )
    ))''')

class TestMe(calliope.Line):
    meter = m
    set_rhythm = (1, 0.5, 3, 4, 3, 0.5, 0.5, 4, 0.75, 7.75, 3, 9, 0.5, 0.5, 2)
    time_signature = (3,4)

t = TestMe()
t.illustrate_me()










