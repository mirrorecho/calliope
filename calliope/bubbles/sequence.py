import importlib, inspect
import calliope

# class MatchSequence(calliope.Bubble):

#     def music(self, **kwargs):
#         if len(self) > 0:
#             initial_bubble = self[0]
#             my_container = initial_bubble.music_container(**kwargs)
#             for initial_sub_item in initial_bubble:
#                 sub_container = initial_sub_item.music_container()
#                 for sequence_bubble in self:
#                     try:
#                         sub_container.append( 
#                             sequence_bubble.child_music(
#                                 sequence_bubble[initial_sub_item.name]
#                                 ) 
#                             )
#                     except:
#                         self.warn("""tried appending matching music, but %s has no child named '%s'""" 
#                             % (sequence_bubble.name, initial_sub_item.name))
#                 my_container.append(sub_container)
#             return my_container
class MatchSequence(calliope.Bubble):
    is_simultaneous = False


# NOTE: this implementation is slick... but all the copies might hurt performance?
# ... try it out and see... 
class MatchSequence(calliope.Bubble):
    is_simultaneous = False

    def music(self, **kwargs):
        return self.get_inverted().music(**kwargs)

    def get_inverted(self):
        return calliope.Bubble(
            *[ calliope.Bubble( 
                *[ b[c.name](name=b.name) for b in self],
                name=c.name,
                is_simultaneous = self.is_simultaneous
                ) for c in self[0] ],
            is_simultaneous = not self.is_simultaneous
            )
