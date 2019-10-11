import abjad, calliope

class CompositeRow(calliope.FromSelectableFactory):
    """
    Creates a new row by merging events from all rows in a block
    """

    branch_type = calliope.Event

    def get_branches(self, *args, **kwargs):

        # create a dictionary of all events in the block with the start time
        # (in ticks) as the key... which removes dupe simultaneous events  
        events_dict = {}
        for r in reversed(self.selectable):
            ticks_counter = 0

            for e in r.events:
                # (notes override rests)
                if ticks_counter not in events_dict or not e.rest:
                    events_dict[ ticks_counter ] = e

                ticks_counter += e.ticks
        
        # create a list of copies events in the dict,
        # ordered by start time and with duration adjusted 

        events_list = []
        previous_e = None
        previous_t = 0

        for t, e in sorted(events_dict.items()):
            my_e = e() # copy the event

            if previous_e:
                previous_e.first_primary_tie.ticks = t - previous_t

            events_list.append(my_e)

            previous_t = t
            previous_e = my_e

        # return the events list as the branches
        return events_list


class SplayRow(calliope.FromSelectableFactory):
    """
    Creates a new block by "splaying" events in a row 
    (alternately assigning across the block's rows)
    """

    branch_type = None # will be set based on the selectable
    num_rows = 3

    def __init__(self, *args, **kwargs):
        self.branch_type = self.child_types[0]
        super().__init__(*args, **kwargs)


    def get_branch(self, index, *args, **kwargs):
        print(self.branch_type, self.selectable)

        return self.branch_type(
            calliope.Poke(selection=self.selectable(lambda sel, i, e: i % self.num_rows==index))(
                    self.selectable
                )
            )

    def get_branches(self, *args, **kwargs):
        return [self.get_branch(i, *args, **kwargs) for i in range(self.num_rows)]



class CompositeCell(CompositeRow, calliope.Cell): pass

class CompositeLine(CompositeRow, calliope.Line): pass

