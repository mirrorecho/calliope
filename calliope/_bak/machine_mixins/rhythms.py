import abjad
from calliope import bubbles, structures, machines


# class Rhythms(object):

#     """
#     mixin that creates rhythms based off of a defined rhythm_sequence, with various trinkets
#     """
#     # metrical_durations = None  # ID(max=4, default=((1,1),))
#     # once_only = True
#     rhythm_segments = (
#         # NOTE... anything >1 can be extended IFF at the beginning/end of a phrase
#         (2, 1, 1),
#         (1, 1, 1),
#         (4, 1, 1),
#     )
#     rhythm_sequence = (
#         0, 1, 2  # these values for testing purposes only
#     )
#     # rhythm_denominator = 32
#     # rhythm_default_multiplier = 8
#     rhythm_times = 1

#     rhythm_initial_silence = 0
#     # multimasure_rests_length = None # (NO LONGER USED)


#     def set_logical_tie(self, logical_tie, **kwargs):
#         super().set_logical_tie(logical_tie, **kwargs)
#         event = logical_tie.parent
#         logical_tie.original_duration = event.parent.rhythm_segment[event.my_index]
#         if logical_tie.original_duration < 0:
#             logical_tie.rest = True
#         logical_tie.ticks = abs(int(logical_tie.original_duration*self.rhythm_default_multiplier))

#     def set_logical_ties(self, event, **kwargs):
#         super().set_logical_ties(event, **kwargs)
#         # (by default, there is just 1 logical tie per event... )
#         self.set_logical_tie( event.branch() )
#         # self.info("setting logical tie", event)
#         event.index_children()

#     def set_event(self, event, **kwargs):
#         super().set_event(event, **kwargs)
#         # TO DO... remove? Any attributes to set for event level for rhythms?

#     def set_events(self, segment, **kwargs):
#         super().set_events(segment, **kwargs)
#         for i in range(len(segment.rhythm_segment)):
#             event=segment.branch()
#             # event.event_index = len(event.root.events)
#             event.root.events.append(event)
#             self.set_event(event, **kwargs)
#             self.set_logical_ties(event, **kwargs)
#         segment.index_children()

#     def set_segment(self, segment, **kwargs):
#         super().set_segment(segment, **kwargs)
#         rhythm_segment_index = self.rhythm_sequence[segment.my_index]
#         segment.rhythm_segment = self.rhythm_segments[rhythm_segment_index]

#     def set_segments(self, **kwargs):
#         super().set_segments(**kwargs)
#         initial_silence_segment = self.data.branch()
#         initial_silence_event = initial_silence_segment.branch()
#         initial_silence_logical_tie = initial_silence_event.branch(
#                     ticks=int(self.rhythm_initial_silence*self.rhythm_default_multiplier), rest=True )
        
#         # now loop through sequence of rhythm segments after the 0'th index:
#         for i in range( (len(self.rhythm_sequence)-1)*self.rhythm_times ):
#             segment = self.data.branch()
#             self.set_segment(segment, **kwargs)
#             self.set_events(segment, **kwargs)
#         self.data.index_children()
    
    # def process_music(self, music, **kwargs):
    #     super().process_music(music, **kwargs)
    #     self.process_logical_ties(music, **kwargs)
    #     self.replace_multimeasure_rests(music)