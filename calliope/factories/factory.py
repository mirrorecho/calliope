import calliope

class Factory(calliope.BaseMixin):
    branch_type = calliope.Cell

    def __init__(self, *args, **kwargs):
        if isinstance(self, calliope.BaseMachine):
            super().__init__(*args, **kwargs)
        else:
            self.setup(*args, **kwargs)

    def get_branches_kwargs(self, *args, **kwargs):
        # should return an iterable of dictionaries
        return () # e.g. return (dict(rhythm=(1,2), pitches=(2,1)), dict(...),)

    def get_branch(self, *args, **kwargs):
        return self.branch_type(**kwargs)

    def get_branches(self, *args, **kwargs):
        return [
            self.get_branch(**branch_kwargs) for branch_kwargs in 
            self.get_branches_kwargs(*args, **kwargs)
            ]

    def fabricate(self, machine, *args, **kwargs):
        machine.extend(self.get_branches(*args, **kwargs))

class EventBranchFactory(Factory):
    branch_type = calliope.Event

    def get_rhythm(self):
        return ()

    def get_pitches(self, rhythm_length):
        return ()

    def get_branches_kwargs(self, *args, **kwargs):
        my_rhythm = self.get_rhythm()
        my_pitches = self.get_pitches(rhythm_length=len(my_rhythm))
        return [dict(beats=b, pitch=p) for b,p in zip(my_rhythm, my_pitches)]

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


