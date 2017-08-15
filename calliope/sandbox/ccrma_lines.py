import abjad
from calliope import tools, bubbles, machines



tools.illustrate_me(bubble = bubble)

# bubble.show()

# class MyCluster(calliope.Bubble):
#     container_type = abjad.Cluster
#     color = "red"

#     class StartCluster(calliope.Bubble):
#         is_simultaneous = False
#         music_contents = "c'1"

#     class EndCluster(calliope.Bubble):
#         is_simultaneous = False
#         music_contents = "e''1"

#     def process_music(self, music, **kwargs):
#         abjad.override(music).note_head.color = self.color

# class MyClusters(calliope.Bubble):
#     times = 1

#     def music(self, **kwargs):
#         my_container = self.container_type()
#         my_container.extend( [ MyCluster().music() for i in range(self.times) ] )
#         return my_container

# class DemoBubble(calliope.Bubble):
#     clusters_3 = MyClusters(times=3)


# tools.illustrate_me( bubble=DemoBubble )


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

# tools.illustrate_me(  )