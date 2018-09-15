import abjad
import calliope

# TO DO... these transforms are super basic... even worth it?

class AddConstantPitch(calliope.Transform):
    """
    Applicable to blocks, adds a new row to the block
    """

    pitch=0

    def transform(self, selectable, **kwargs):
        new_child = selectable[0](name=str(selectable.name) + "constant_pitch_" + str(self.pitch))
        for event in new_child.non_rest_events:
            event.pitch = self.pitch

        selectable.append(new_child)