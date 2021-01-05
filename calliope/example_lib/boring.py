import calliope


@calliope.register
class SimpleCell(calliope.Cell):
    init_rhythm = (1, 1, 2, 2, 4, 4)
    init_pitches = (0, 2, 4, 5, 4, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# The following three examples produce identical results... the approach to choose would depend
# on the particular use case...


@calliope.register
class SimplePhrase1(calliope.Phrase):
    @calliope.register
    class Cell1(SimpleCell):
        def decorate(self):
            return self.e_ops(
                0, "p", "\\<")(
                4, "f")()

    @calliope.register
    class Cell2(SimpleCell):
        pass

    def decorate(self):
        self.e_ops(
            0, "p", "\\<")(
            4, "f")()

    def make_fancy(self, ):
        self.events[1].pitch += 2
        self.events[-1].pitch -= 2
        self.sc(0.5)


@calliope.register
def simple_phrase2(lib):
    return calliope.Phrase(
        SimpleCell(),
        SimpleCell(),
    )


@calliope.register
def simple_phrase3(lib):
    return lib("boring.simple_cell").mul(2, wrap_in=calliope.Phrase)

