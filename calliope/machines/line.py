import calliope

class Line(calliope.FragmentRow):
    child_types = (calliope.Phrase, calliope.Cell, calliope.Event)
    select_property = "lines"