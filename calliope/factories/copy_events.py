import calliope

class CopyEventsFactory(calliope.Factory):
    selectable = None

    def get_branches(self, *args, **kwargs):
        return [e() for e in self.selectable.events]


