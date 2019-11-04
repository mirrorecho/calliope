import abjad
import calliope

c  = calliope.Cell(
    rhythm = (-1, -2, -1, -1, 2, 3, -4),
    pitches = (2, 4, ),
    pitches_skip_rests = True,
    )

# c.events[1].skip=True

c.pitches = (2,4)
c.events[4].pitch = 6

class MySkip(calliope.Event):
    init_beats = 4
    # init_rest = True
    init_skip = True

m = MySkip(rest=True)

# m.rest=True

c.events[0].skip=True
print(c.events[0].skip)


calliope.illustrate(
    calliope.Segment(
        # MySkip(),
        # MySkip(),
        # m(),
        # c(pitches=(1,2,3), pitches_skip_rests=False),
        # c(),
        c(),
    )
    )