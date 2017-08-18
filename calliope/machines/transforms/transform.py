import abjad
import calliope

class Transform(calliope.Tree):

    def _transform_setup(self, bubble):
        self.transform_setup(bubble)
        for c in self.children:
            c._transform_setup(bubble)

    def _transform_nodes(self, bubble):
        self.transform_nodes(bubble)
        for c in self.children:
            c._transform_nodes(bubble)

    def transform_setup(self, bubble):
        pass

    def transform_nodes(self, bubble):
        pass
