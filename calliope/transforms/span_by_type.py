import abjad
import calliope

class SpanByType(calliope.Transform):
    by_type = None
    start_span = "("
    stop_span = ")"

    def transform(self, selectable, **kwargs):
        for node in selectable.select_by_type(self.by_type):
            if len(node.note_events) > 1:
                node.note_events[0].tag(self.start_span)
                node.note_events[-1].tag(self.stop_span)
 
# NOTE: this doesn't work... why?
class BracketCells(SpanByType):
    by_type = calliope.Cell
    start_span = "{"
    stop_span = "}"

class SlurCells(SpanByType):
    by_type = calliope.Cell


class PhrasePhrases(SpanByType):
    by_type = calliope.Phrase
    start_span = "(("
    stop_span = "))"