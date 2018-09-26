import calliope

class CopyEventsFactory(calliope.Factory):
    selection = None

    def get_branches(self, *args, **kwargs):
        return [e() for e in self.selection.events]


