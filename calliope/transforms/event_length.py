import abjad
import calliope

# TO DO... these transforms are super basic... even worth it?
class EventLength(calliope.Transform):
    set_length = None
    scale_length = 1
    increase_length = 0


    def transform(self, selectable, **kwargs):
        last_selectable = selectable[-1]
        my_index = last_selectable.my_index
        my_parent = last_selectable.parent
        
        event_list = list(selectable.events)

        for j in range(self.times):
            for i, event in enumerate(event_list):
                my_parent.insert(my_index+i+1, event())



class Displace(calliope.Transform):
    interval = 12
    multiple = 1

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            event.transpose(self.interval * self.multiple)

class DisplaceFifths(Displace):
    interval = 7