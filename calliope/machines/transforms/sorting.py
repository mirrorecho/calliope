import abjad
import calliope

class Sorting(calliope.Transform):
    reverse = False

    def key_method(self, item):
        return item.index

    def transform(self, selectable, **kwargs):
        machine[:] = sorted( machine, key = lambda e : self.key_method(e), reverse=self.reverse)


class SortByPitch(Sorting):
    def key_method(self, item):
        pitch = item.pitch
        if isinstance(item, (list, tuple)):
            pitch = pitch[0]
        return abjad.NumberedPitch(pitch).number   


class SortByDuration(Sorting):
    def key_method(self, item):
        return item.ticks

