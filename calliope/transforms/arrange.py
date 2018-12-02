import abjad
import calliope

class Arrange(calliope.Transform):
    from_selectable = None
    destination_args = ()

    def get_detination_branches(self, selectable):
        if self.detination_branch_names:
            return selectable[*self.detination_branch_names]
         else: 
            selectable.select

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            event.transpose(self.interval)