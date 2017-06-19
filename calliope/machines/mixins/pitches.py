# import copy
# import abjad


# class Pitches(object):
#     pitch_segments = ( # TO DO... better to use IndexedData for this?
#             # TO CONSIDER... CHANGE UP THE PITCH SEGMENTS:
#             # ( 2, 0,-2), #0
#             # (-5,-4,-2), #1
#             # (-3, 0,-2), #2
#             # ( 2, 0,-1), #3
#             # (-5,-3,-1), #4
#             # (-3, 0,-1), #5
#             ( 2, 0,-1), #0
#             (-5,-3,-1), #1
#             (-3, 0,-1), #2
#         )
#     pitch_sequence = (0,1,2) # for testing only

#     def respell_events(self, spelling, start_index=None, stop_index=None):
#         for e in self.events[start_index:stop_index]:
#             e.respell = spelling

#     def set_event(self, event, **kwargs):
#         super().set_event(event, **kwargs)
#         if event.parent.pitch_segment: # need to test for this because harmony wouldn't have set pitch segment on parent
#             # TO DO... this could be more elegant... Use cyclic Indexed Data? for pitch segments?
#             event.original_pitch = event.parent.pitch_segment[event.my_index % len (event.parent.pitch_segment)]
#             event.pitch = event.original_pitch

#     def set_segment(self, segment, **kwargs):
#         super().set_segment(segment, **kwargs)
#         pitch_segment_index = self.pitch_sequence[segment.my_index]
#         segment.pitch_segment = self.pitch_segments[pitch_segment_index]

#     # def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_count, **kwargs):
#     #     super().process_logical_tie(music, music_logical_tie, data_logical_tie, music_leaf_count, **kwargs)
#     #     if not data_logical_tie.rest:
#     #         event = data_logical_tie.parent
#     #         pitch = event.pitch
#     #         if  isinstance(pitch, (list, tuple)):
#     #             if event.respell=="flats":
#     #                 named_pitches = [abjad.NamedPitch(p).respell_with_flats() for p in pitch]
#     #             elif event.respell=="sharps":
#     #                 named_pitches = [abjad.NamedPitch(p).respell_with_sharps() for p in pitch]
#     #             else:
#     #                 named_pitches = [abjad.NamedPitch(p) for p in pitch]
#     #             # NOTE, decided to implement here (as opposed to in harmony machine), because want chords to be able to be implemented generally
#     #             for note in music_logical_tie:
#     #                 chord = abjad.Chord()
#     #                 chord.note_heads = named_pitches
#     #                 chord.written_duration = copy.deepcopy(note.written_duration)
#     #                 m = abjad.mutate([note])
#     #                 m.replace(chord)
#     #         elif isinstance(pitch, int):
#     #             if event.respell=="flats":
#     #                 named_pitch = abjad.NamedPitch(pitch).respell_with_flats()
#     #             elif event.respell=="sharps":
#     #                 named_pitch = abjad.NamedPitch(pitch).respell_with_sharps()
#     #             else:
#     #                 named_pitch = abjad.NamedPitch(pitch)
#     #             for note in music_logical_tie:
#     #                 note.written_pitch = named_pitch
#     #         else:
#     #             self.warn("can't set pitch because '%s' is not int, list, or tuple" % pitch,  data_logical_tie )
