from calliope import machines

class Cell(machines.Machine):
    child_types = (machines.Event,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "rhythm" in kwargs:
            for i, r in enumerate(kwargs["rhythm"]):
                if "pitches" in kwargs:
                    pitch = kwargs["pitches"][i % len(kwargs["pitches"]) ]
                print(r)
                self["r%s" % i] = machines.Event(beats=r, pitch=pitch)