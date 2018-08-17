import calliope

class Factory(calliope.CalliopeBaseMixin):

    def __init__(self, *args, **kwargs):
        if isinstance(self, calliope.BaseMachine):
            super().__init__(*args, **kwargs)
        else:
            self.setup(*args, **kwargs)

    def fabricate(self, machine, *args, **kwargs):
        pass

