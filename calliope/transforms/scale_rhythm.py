import abjad
import calliope

class ScaleRhythm(calliope.Transform):
    scale = 1 

    def transform(self, selectable, **kwargs):
        for event in selectable.events:
            event.beats = event.beats * self.scale
