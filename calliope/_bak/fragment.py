import abjad
import calliope


# TO DO: CONSIDER SOME OTHER  EASY WAY OF ADDING CUSTOM MUSIC CONTENTS...
# class Fragment(calliope.Bubble):
#     """
#     A fragment of (ususually) horizontal music. Includes conveniences like
#     specifiying time signature, spelling, clef, etc.
#     """

#     # transpose = 0 # TO CONSIDER: bring back transpose at this level? (assume no)

#     def __init__(self, *args, **kwargs):
#         """
#         overriding __init__ simply to be able to use music_contents as a positional argument
#         """
#         if len(args) > 0 and type(args[0]) is str:
#             self.music_contents = args[0]
#             args = args[1:]
#         super().__init__(*args, **kwargs)



    # TO DO: this is experimental only at the moment...
    # def free_box(self, arrows=0, **kwargs):
    #     return_bubble = copy(self)
    #     return_bubble.commands = [c for c in self.commands]
    #     return_bubble.commands.append( ("freeOn", "before") )
    #     # return_bubble.commands.append( ("leftBracket", "before") )
    #     if not arrows:
    #         return_bubble.commands.append( ("freeAfter", "after") )
    #     return_bubble.commands.append( ("freeOff", "after") )
    #     return return_bubble


# class SegmentMixin(object):
#     """
#     intended to be used with Fragment, SegmentMixin implements some conveniences useful for longer
#     segments of music (e.g. adding rehearsal marks).
#     """
#     child_types = (Fragment, )
#     tempo_text = None
#     tempo_units_per_minute=None
#     tempo_duration=(1,4) # only used if tempo_units_per_minute also specified
#     tempo_command = None
#     rehearsal_mark_number = None
#     compress_full_bar_rests = None # TO DO... maybe this should be handled somewhere else? (currently it's being repeated where not necessary... at the beginning of every line)
#     accidental_style = "modern-cautionary" # TO DO... necessary?

#     def process_music(self, music, **kwargs):
#         Fragment.process_music(self, music, **kwargs)
#         if len(music) > 0:
#             music_start = music[0]
            
#             if self.rehearsal_mark_number:
#                 mark = abjad.RehearsalMark(number=self.rehearsal_mark_number)
#                 abjad.attach(mark, music_start)
#             # NOTE... True adds command to compress, False adds compand to expand, None does nothing
            
#             if self.compress_full_bar_rests == True:
#                 rests_command =  abjad.LilyPondLiteral(r"\compressFullBarRests", "before")
#                 abjad.attach(rests_command, music_start)

#             elif self.compress_full_bar_rests == False:
#                 rests_command =  abjad.LilyPondLiteral(r"\expandFullBarRests", "before")
#                 abjad.attach(rests_command, music_start)

#             # TO DO... TEMPO MAKES EVERYTHING SLOW... WHY?
#             if self.tempo_text or self.tempo_units_per_minute:
#                 if self.tempo_units_per_minute:
#                     tempo_reference_duration = Duration(self.tempo_duration)
#                 else:
#                     tempo_reference_duration = None
#                 tempo = abjad.Tempo(tempo_reference_duration, units_per_minute=self.tempo_units_per_minute, textual_indication=self.tempo_text)
#                 abjad.attach(tempo, music_start)

#             elif self.tempo_command:
#                 tempo_command =  abjad.LilyPondLiteral(r"\tempo \markup \fontsize #3 { %s }" % self.tempo_command, "before")
#                 # print(tempo_command)
#                 abjad.attach(tempo_command, music_start)

#             if self.accidental_style:
#                 accidental_style_command = abjad.LilyPondLiteral(r"\accidentalStyle " + self.accidental_style, "before")
#                 abjad.attach(accidental_style_command, music_start)

# class Segment(SegmentMixin, Fragment):
#     pass

# class MultiFragment(Fragment):
#     """
#     a fragment with temporary simultaneous music... optionally as multiple voices
#     """
#     multi_voiced = True
#     is_simultaneous = True
#     instruction = None

#     def child_music(self, child_bubble):
#         my_music = self.container_type()
#         my_music.append( child_bubble.blow() )
#         return my_music

#     def music(self, **kwargs):
#         # TO DO... test this!!!!!!
#         my_music = super().music(**kwargs)

#         if self.multi_voiced and len(my_music) > 1:
#             for container in my_music[0:-1]:
#                 command_voices = abjad.LilyPondLiteral('\\ ', 'after')
#                 abjad.attach(command_voices, container)
#             command_one_voice = abjad.LilyPondLiteral(r'\oneVoice', 'after')
#             abjad.attach(command_one_voice, my_music)
#         return my_music

# class SimulFragment(MultiFragment):
#     """
#     same as MultiFragment, but defaults multi_voiced to False
#     """
#     multi_voiced = False

