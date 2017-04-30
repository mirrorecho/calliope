from calliope import machines


# minumum needed for any basic line with rhythms & pitches, with no special manipulations applied
class PitchedMachine(machines.AttachTags, machines.Pitches, machines.Rhythms, machines.Machine):
    compress_full_bar_rests = True

# minumum needed for any basic line with rhythms only, with no special manipulations applied
class RhythmicMachine(machines.AttachTags, machines.Rhythms, machines.Machine):
    compress_full_bar_rests = True

class ArrangeMachine(machines.Arrange, PitchedLine):
	pass