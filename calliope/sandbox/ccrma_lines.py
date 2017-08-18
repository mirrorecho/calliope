import abjad
import calliope




# calliope.illustrate_me(bubble = bubble)

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


# calliope.illustrate_me( bubble=DemoBubble )








# ==============================================

# calliope.illustrate_me(  )