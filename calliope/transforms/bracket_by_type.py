import abjad
import calliope

class BracketByType(calliope.Transform):
    by_type = None

    def transform(self, selectable, **kwargs):
        for node in selectable.by_type(self.by_type):
            if len(node) > 1:
                node.logical_ties[0].tag("{")
                node.logical_ties[1].tag("}")
 

class BracketCells(BracketByType):
    by_type = calliope.Cell