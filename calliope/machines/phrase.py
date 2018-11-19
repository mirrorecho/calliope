import calliope

class Phrase(calliope.EventMachine):
    child_types = (calliope.Cell, calliope.Event)
    select_property = "phrases"