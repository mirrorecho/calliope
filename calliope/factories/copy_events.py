import calliope

class CopyEventsFactory(calliope.Factory):
    selection = None

    def fabricate(self, machine, *args, **kwargs):
        # TO DO... rename all these events?
        machine.extend([e() for e in self.selection.events])
