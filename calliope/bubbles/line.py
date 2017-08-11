import abjad
from calliope import bubbles


class Line(bubbles.Bubble):
    """
    Bubble factory for an abjad Container with a single line of music
    """
    is_simultaneous = False
    music_string = None
    tempo_text = None
    tempo_units_per_minute=None
    tempo_duration=(1,4) # only used if tempo_units_per_minute also specified
    tempo_command = None
    clef = None
    time_signature = None
    start_bar_line = None
    rehearsal_mark_number = None
    accidental_style = "modern-cautionary" # TO DO... necessary?
    compress_full_bar_rests = None # TO DO... maybe this should be handled somewhere else? (currently it's being repeated where not necessary... at the beginning of every line)
    transpose = None
    

    def __init__(self, *args, **kwargs):
        """
        overriding __init__ simply to be able to use music_string as a positional argument
        """
        if len(args) > 0 and type(args[0]) is str:
            self.music_string = args[0]
            args = args[1:]
        super().__init__(*args, **kwargs)

    # def __add__(self, other):
    #     return bubbles.LineSequence( bubbles=(self, other) )

    # def __mul__(self, num):
    #     return bubbles.LineSequence( bubbles = [self for i in range(num)] )

    def music(self, **kwargs):
        if self.music_string:
            my_music = self.container_type( self.music_string )
            # self.container_type = type(my_music) # TO DO: necessary?
            self.is_simultaneous = my_music.is_simultaneous # TO DO: necessary?
            return my_music
        else:
            return super().music(**kwargs)

    def process_music(self, music, **kwargs):
        if len(music) > 0:
            music_start = music[0]

            # TO DO... keep this...???
            # if self.transpose:
            #     abjad.mutate(music).transpose(self.transpose)

            if self.time_signature:
                # TO DO... is the numeric comm*ad necessary... maybe just include it at the score level?
                time_command_numeric =  abjad.indicatortools.LilyPondCommand("numericTimeSignature", "before")
                abjad.attach(time_command_numeric, music_start)

                time_command =  abjad.indicatortools.LilyPondCommand("time " + str(self.time_signature[0]) + "/" + str(self.time_signature[1]), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(time_command, music)
            if self.clef:
                clef_obj = abjad.Clef(self.clef)
                abjad.attach(clef_obj, music_start)
            if self.start_bar_line:
                bar_command =  abjad.indicatortools.LilyPondCommand('bar "' + self.start_bar_line + '"', 'before')
                abjad.attach(bar_command, music_start)
            if self.rehearsal_mark_number:
                mark = abjad.indicatortools.RehearsalMark(number=self.rehearsal_mark_number)
                abjad.attach(mark, music_start)
            # NOTE... True adds command to compress, False adds compand to expand, None does nothing
            if self.compress_full_bar_rests == True:
                rests_command =  abjad.indicatortools.LilyPondCommand("compressFullBarRests", "before")
                abjad.attach(rests_command, music_start)
            elif self.compress_full_bar_rests == False:
                rests_command =  abjad.indicatortools.LilyPondCommand("expandFullBarRests", "before")
                abjad.attach(rests_command, music_start)

            # TO DO... TEMPO MAKES EVERYTHING SLOW... WHY?
            if self.tempo_text or self.tempo_units_per_minute:
                if self.tempo_units_per_minute:
                    tempo_reference_duration = Duration(self.tempo_duration)
                else:
                    tempo_reference_duration = None
                tempo = abjad.indicatortools.Tempo(tempo_reference_duration, units_per_minute=self.tempo_units_per_minute, textual_indication=self.tempo_text)
                abjad.attach(tempo, music_start)
            elif self.tempo_command:
                tempo_command =  abjad.indicatortools.LilyPondCommand("tempo \markup \\fontsize #3 { %s }" % self.tempo_command, "before")
                # print(tempo_command)
                abjad.attach(tempo_command, music_start)
            if self.accidental_style:
                accidental_style_command = abjad.indicatortools.LilyPondCommand("accidentalStyle " + self.accidental_style, "before")
                abjad.attach(accidental_style_command, music_start)
            super().process_music(music, **kwargs)

    def free_box(self, arrows=0, **kwargs):
        return_bubble = copy(self)
        return_bubble.commands = [c for c in self.commands]
        return_bubble.commands.append( ("freeOn", "before") )
        # return_bubble.commands.append( ("leftBracket", "before") )
        if not arrows:
            return_bubble.commands.append( ("freeAfter", "after") )
        return_bubble.commands.append( ("freeOff", "after") )
        return return_bubble


class MultiLine(Line):
    """
    a line with temporary simultaneous music... optionally as multiple voices
    """
    multi_voiced = True
    is_simultaneous = True
    instruction = None

    def child_music(self, child_bubble):
        my_music = self.container_type()
        my_music.append( child_bubble.blow() )
        return my_music

    def music(self, **kwargs):
        my_music = super().music(**kwargs)

        if self.multi_voiced and len(my_music) > 1:
            for container in my_music[0:-1]:
                command_voices = abjad.indicatortools.LilyPondCommand('\\ ', 'after')
                abjad.attach(command_voices, container)
            command_one_voice = abjad.indicatortools.LilyPondCommand('oneVoice', 'after')
            abjad.attach(command_one_voice, my_music)
        return my_music

class SimulLine(MultiLine):
    """
    same as MultiLine, but defaults multi_voiced to False
    """
    multi_voiced = False

