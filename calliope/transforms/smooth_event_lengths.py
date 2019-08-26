import abjad
import calliope

class SmoothEventLength(calliope.Transform):
 
    # TO DO THiS IS A COPY FROM ANOTHER TRANFORM... DOES NOT WORK YET
    # ---------------------
    # ---------------------
    # ---------------------

    def transform(self, selectable, **kwargs):
        last_selectable = selectable[-1]
        my_index = last_selectable.my_index
        my_parent = last_selectable.parent
        
        event_list = list(selectable.events)

            for i, event in enumerate(event_list):
                my_parent.insert(my_index+i+1, event())

