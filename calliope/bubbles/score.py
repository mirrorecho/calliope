import inspect
import abjad
import calliope

class Score(calliope.Bubble):
     # NOTE: abjad.Score.__init__ does not take is_simultaneous as an argument,
    # so it needs to be set to be set to None here
    is_simultaneous = None
    container_type=abjad.Score
    child_types=(calliope.StaffGroup, calliope.Staff)
    # TO DO... the following are no longer used... keep them?
    hide_empty = False 
    title = ""

    @classmethod
    def startup_root(cls):
        calliope.Staff.child_types = (calliope.Segment, calliope.Line, calliope.Phrase, calliope.Cell, calliope.Event) 
        calliope.Voice.child_types = (calliope.Segment, calliope.Line, calliope.Phrase, calliope.Cell, calliope.Event)         

        super().startup_root()

        calliope.Cell.set_tree_select_property("note_events", 
            lambda x: x.select_by_type(calliope.Event).exclude(skip_or_rest=True)
            ) 

        calliope.Cell.set_tree_select_property("rest_events", 
            lambda x: x.select_by_type(calliope.Event)(rest=True)
            ) 

        calliope.Cell.set_tree_select_property("skip_events", 
            lambda x: x.select_by_type(calliope.Event)(skip=True)
            ) 

        # TO DO: needed?
        # calliope.Cell.set_tree_select_property( "select_cells",
        #     lambda x: calliope.Selection(select_from=x.children, type_args=(calliope.Cell,))
        #     )


    def process_music(self, music, **kwargs):

        super().process_music(music, **kwargs)
        self.info("created abjad music container object for the score")


# TO DO EVENTUALLY: rethink this as a factory
# class AutoScore(Score):
#     def set_children(self, parent_bubble, copy_children_from):
#         if parent_bubble is self: # tests whether we're at the top-level or recursively calling set_children
#             for bubble in copy_children_from:
#                 self[bubble.name] = calliope.Staff(
#                     instrument=abjad.Instrument(
#                         name=bubble.name, 
#                         short_name=bubble.name)
#                     )
#         super().set_children(parent_bubble, copy_children_from)


