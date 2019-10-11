import calliope

# TO DO: keep base factory SIMPLE... only needs to implement fabricate
class Factory(calliope.CalliopeBase):
    branch_type = calliope.Cell # TO DO: this isn't used all the time KISS

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

class FromSelectableFactory(Factory):
    selectable = None # TO CONSIDER: should this be sub_selectable?

    def __init__(self, selectable=None, *args, **kwargs):
        self.selectable = selectable or self.selectable
        super().__init__(*args, **kwargs)

    def get_branch(self, node, *args, **kwargs):
        return node(*args, **kwargs)

    def get_branches(self, *args, **kwargs):
        return [self.get_branch(n, *args, **kwargs) for n in self.selectable]

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

# class Factory(calliope.CalliopeBase):
#     factory_rhythm = ()
#     factory_pitches = ()

#     def get_rhythm(self):
#         return self.factory_rhythm

#     def get_pitches(self):
#         return self.factory_pitches

#     def fabricate(self, machine, *args, **kwargs):
#         machine.rhythm = self.get_rhythm()
#         machine.pitches = self.get_pitches()


