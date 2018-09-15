import calliope

class Factory(calliope.BaseMixin):
    branch_type = calliope.Event

    def __init__(self, *args, **kwargs):
        if isinstance(self, calliope.BaseMachine):
            super().__init__(*args, **kwargs)
        else:
            self.setup(*args, **kwargs)

    def get_branches(self):
        return [e() for e in self.selection.events]

    def fabricate(self, machine, *args, **kwargs):
        machine.rhythm = self.get_rhythm()
        machine.pitches = self.get_pitches()

# class Factory(calliope.BaseMixin):
#     factory_rhythm = ()
#     factory_pitches = ()

#     def __init__(self, *args, **kwargs):
#         if isinstance(self, calliope.BaseMachine):
#             super().__init__(*args, **kwargs)
#         else:
#             self.setup(*args, **kwargs)

#     def get_rhythm(self):
#         return self.factory_rhythm

#     def get_pitches(self):
#         return self.factory_pitches

#     def fabricate(self, machine, *args, **kwargs):
#         machine.rhythm = self.get_rhythm()
#         machine.pitches = self.get_pitches()


