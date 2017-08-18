import abjad
from calliope import tools, bubbles, machines

class ClusterNote(calliope.Bubble):
    leaf_string="c'4"
    def __init__(self, leaf_string=None, *args, **kwargs):
        if leaf_string:
            self.leaf_string = leaf_string

class ClusterBase(calliope.Bubble):
    container_type = abjad.Cluster
    is_simultaneous = False
    sub_types = (ClusterNote, )

    def child_music(self, child_bubble):
        child_note = abjad.Note()
        child_note.written_pitch = abjad.NamedPitch(child_bubble.pitch)
        return child_note

class Cluster1(ClusterBase):
    start = ClusterNote(pitch="C1")
    middle = ClusterNote(pitch="A7")
    end = ClusterNote(pitch="B4")

class Clusters(calliope.Bubble):
    cluster_types = ()
    is_simultaneous = False
    times =1

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.cluster_types = args
        self.extend( [c()() for c in self.cluster_types] )

class DemoBubble(calliope.Bubble):
    clusters_I = Clusters(Cluster1,)


calliope.illustrate_me( bubble=DemoBubble )


# class ScoreDemo(bubbles.Score):

#     class Flute(bubbles.Staff):
#         instrument=abjad.instrumenttools.Flute(
#             instrument_name="Flute", short_instrument_name="fl.")

#     class Clarinet(bubbles.Staff):
#         instrument=abjad.instrumenttools.ClarinetInBFlat(
#             instrument_name="Clarinet in Bb", short_instrument_name="cl.")

#     class MyStaffGroup(bubbles.StaffGroup):
#         class Violin1(bubbles.Staff):
#             instrument=abjad.instrumenttools.Violin(
#                 instrument_name="Violin 1", short_instrument_name="vln.")

#         class Violin2(bubbles.Staff):
#             instrument=abjad.instrumenttools.Violin(
#                 instrument_name="Violin 2", short_instrument_name="vln.")



# ==============================================

# calliope.illustrate_me(  )