import calliope

class Phrase(calliope.FragmentRow):
    child_types = (calliope.Cell, calliope.Event)
    select_property = "phrases"