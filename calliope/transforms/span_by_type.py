import abjad
import calliope

class SpanByType(calliope.Transform):
    by_type = None
    start_span = "{"
    stop_span = "}"

    def transform(self, selectable, **kwargs):
        for node in selectable.by_type(self.by_type):
            if len(node) > 1:
                node.logical_ties[0].tag(self.start_span)
                node.logical_ties[-1].tag(self.stop_span)
 

class BracketCells(SpanByType):
    by_type = calliope.Cell

class SlurCells(SpanByType):
    by_type = calliope.Cell
    start_span = "("
    stop_span = ")"