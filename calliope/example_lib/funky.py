import calliope


@calliope.register
class FancyCell(calliope.Cell):
    init_rhythm = (0.25, 1, 0.25, 0.5, 3, 3)
    init_pitches = (6, 5, 4, 7, 9, 1)