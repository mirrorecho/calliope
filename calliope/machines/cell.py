from calliope import machines

class Cell(machines.Machine):
    child_types = ()

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (machines.Cell, machines.Event)
        super().__init__(*args, **kwargs)

        if "rhythm" in kwargs:
            for i, r in enumerate(kwargs["rhythm"]):
                if "pitches" in kwargs:
                    pitch = kwargs["pitches"][i % len(kwargs["pitches"]) ]
                self["r%s" % i] = machines.Event(beats=r, pitch=pitch)