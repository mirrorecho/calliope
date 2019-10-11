import abjad
import calliope

# TO DO: this would be cleaner with abstract selections
class Overlay(calliope.Transform):
    """
    keeps events in the selection, makes everything else rests
    """
    selection = None

    def transform(self, selectable, **kwargs):

        events_dict = {}
        ticks_counter = 0
        for e in selectable.events:
            events_dict[ ticks_counter ] = e
            ticks_counter += e.ticks

        ticks_counter = 0
        for e in self.selection.events:
            # (notes override rests)
            if ticks_counter not in events_dict or not e.rest:
                events_dict[ ticks_counter ] = e()
            ticks_counter += e.ticks

        events_list = []
        previous_e = None
        previous_t = 0

        for t, e in sorted(events_dict.items()):
            # copy the event?? (assume no)

            if previous_e:
                previous_e.beats = (t - previous_t) / calliope.MACHINE_TICKS_PER_BEAT
            
            # print(t, previous_t, e, )

            events_list.append(e)

            previous_t = t
            previous_e = e

        selectable.clear()
        selectable.extend(events_list)

        
        
