import abjad
import calliope


calliope.illustrate(calliope.Score(
    calliope.RhythmicStaff(
        calliope.Segment(
            calliope.Cell(
            rhythm=(-1,2,2,-1),
            pitches=("S",0,0,"S")
            ),
            time_signature=(8,4),
            metrical_durations=((1,4),(2,4),(2,4),(1,4))
            )
        )
    )
)