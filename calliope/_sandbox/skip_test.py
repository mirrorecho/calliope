import abjad
import calliope

c  = calliope.Cell(
    rhythm = (1,2,-3,4),
    pitches = (2, "S", ),
    pitches_skip_rests = True,
    )

# c.events[0].skip=True
# print(c.events[0])
# print(c.events[0][0])

# c.pitches = (2,4)
# c.events[4].pitch = 6

class MySkip(calliope.Event):
    init_beats = 3
    # init_rest = True
    init_skip = True

m0 = MySkip()
m = MySkip(rest=True)

s = calliope.Segment(
    MySkip(),
    MySkip(),
    m(),
    MySkip(),
    m(),
    MySkip(),
    # m(),
    # c(pitches=(1,2,3), pitches_skip_rests=False),
    c(),
    c(),
)

s.note_events.tag("N")
s.rest_events.tag("R")
s.skip_events.tag("S")


calliope.illustrate(s)