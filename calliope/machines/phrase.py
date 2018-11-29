import calliope

class Phrase(calliope.FragmentLine):
    child_types = (calliope.Cell, calliope.Event)
    select_property = "phrases"