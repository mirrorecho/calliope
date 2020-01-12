import abjad, calliope

class CompositeChordsRow(calliope.FromSelectableFactory):
    branch_type = calliope.Event

    def get_branches(self, *args, **kwargs):

        # create a dictionary of all events in the block with the start time
        # (in ticks) as the key... which removes dupe simultaneous events  
        pitches_dict = {}
        for r in reversed(self.selectable):
            ticks_counter = 0

            for e in r.events:
                # (notes override rests)
                if ticks_counter in pitches_dict:
                    pitches_dict[ ticks_counter ] -= set(("R",))
                    pitches_dict[ ticks_counter ] |= e.pitch_set 
                else:
                    pitches_dict[ ticks_counter ] = e.pitch_set

                ticks_counter += e.ticks
        
        # create a list of copies events in the dict,
        # ordered by start time and with duration adjusted 

        events_list = []
        previous_e = None
        previous_t = 0

        for t, e in sorted(pitches_dict.items()):
            e_pitch = list(sorted(e))
            if len(e_pitch) == 1:
                e_pitch = e_pitch[0]
            my_e = calliope.Event(pitch=e_pitch) # copy the event

            if previous_e:
                previous_e.first_primary_tie.ticks = t - previous_t

            events_list.append(my_e)

            previous_t = t
            previous_e = my_e

        # final event ticks
        previous_e.first_primary_tie.ticks = self.selectable.ticks - t

        # return the events list as the branches
        return events_list

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


class SplayBlock(calliope.FromSelectableFactory):
    """
    Creates a new block by "splaying" events in a row 
    (alternately assigning across the block's rows)
    """

    branch_type = None # will be set based on the selectable
    num_rows = 3

    def get_branch(self, index, *args, **kwargs):
        my_row = self.selectable()
        my_row.note_events(lambda sel, i, e: (i % self.num_rows)!=index).setattrs(rest=True)
        return my_row


    def get_branches(self, *args, **kwargs):
        return [self.get_branch(i, *args, **kwargs) for i in range(self.num_rows)]

class CompositeChordsCell(CompositeChordsRow, calliope.Cell): pass

class CompositeChordsLine(CompositeChordsRow, calliope.Line): pass

class CompositeCell(CompositeRow, calliope.Cell): pass

class CompositeLine(CompositeRow, calliope.Line): pass

class SplayLineBlock(SplayBlock, calliope.LineBlock):
    branch_type = calliope.Line

class SplaySegmentBlock(SplayBlock, calliope.SegmentBlock):
    branch_type = calliope.Segment


