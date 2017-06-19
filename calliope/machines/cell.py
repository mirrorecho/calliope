from calliope import machines

class Cell(machines.Machine):
    # pitch_segment = None
    # rhythm_segment = None
    # pitch_reverse = False
    # rhythm_reverse = False
    # rhythm_multiplier = None
    child_types = (machines.Event,)