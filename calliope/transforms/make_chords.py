import abjad
import calliope

class MakeChords(calliope.Transform):
    indices = ()

    def transform_nodes(self, machine):
        # TO DO: NOTE: can blow up with rests
        return_events = []
        for i in self.indices:
            if type(i) is int:
                return_events.append( machine[i]() )
            elif isinstance(i, (list, tuple)):
                return_events.append( machine[ i[0] ]( pitch=[ machine[p].pitch for p in i ] ) )
        machine[:] = return_events