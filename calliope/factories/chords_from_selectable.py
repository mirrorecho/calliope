import calliope

class ChordsFromSelectable(calliope.FromSelectableFactory):
    branch_type = None # uses branch type to wrap events (could be blank)

    def get_branch(self, node, *args, **kwargs):
        chord_event = calliope.Event(beats=node.beats, pitch=sorted(node.pitch_set-set((None,))) )
        if self.branch_type:
            return self.branch_type(chord_event)
        return chord_event