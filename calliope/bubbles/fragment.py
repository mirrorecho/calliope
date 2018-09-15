import abjad
import calliope

class Fragment(calliope.Bubble):
    """
    A fragment of (ususually) horizontal music. Includes conveniences like
    specifiying time signature, spelling, clef, etc.
    """
    is_simultaneous = False
    time_signature = None
    pickup = None # must be able to be represented as a single note with no dots
    clef = None
    bar_line = None
    respell = None # set to "sharps" or "flats"  to force respelling
    # transpose = 0 # TO CONSIDER: bring back transpose at this level? (assume no)

    def __init__(self, *args, **kwargs):
        """
        overriding __init__ simply to be able to use music_contents as a positional argument
        """
        if len(args) > 0 and type(args[0]) is str:
            self.music_contents = args[0]
            args = args[1:]
        super().__init__(*args, **kwargs)

    # def __add__(self, other):
    #     return calliope.LineSequence( bubbles=(self, other) )

    # def __mul__(self, num):
    #     return calliope.LineSequence( bubbles = [self for i in range(num)] )

    # TO DO... apply this same idea more generally for fragments in side of 
    # fragment blocks for things like time_signature
    def get_respell(self):
        if self.respell:
            return self.respell
        elif self.parent and isinstance(self.parent, Fragment):
            return self.parent.get_respell()


    def process_music(self, music, **kwargs):
        super().process_music(music, **kwargs)

        if len(music) > 0:
            music_start = music[0]

            # TO DO... keep this...???
            # if self.transpose:
            #     abjad.mutate(music).transpose(self.transpose)

            # if self.respell:
            #     calliope.respell(music, self.respell)

            if self.time_signature:
                # TO DO... is the numeric comm*ad necessary... maybe just include it at the score level?
                time_command_numeric =  abjad.LilyPondLiteral(r"\numericTimeSignature", "before")
                abjad.attach(time_command_numeric, music_start)

                time_command =  abjad.LilyPondLiteral(r"\time " + str(self.time_signature[0]) + "/" + str(self.time_signature[1]), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(time_command, music_start)

            if self.pickup:
                partial_value = int((1 / self.pickup) * self.rhythm_denominator / self.rhythm_default_multiplier)
                partial_command =  abjad.LilyPondLiteral(r"\partial " + str(partial_value), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(partial_command, music_start)

            if self.clef:
                clef_obj = abjad.Clef(self.clef)
                abjad.attach(clef_obj, music_start)

            if self.bar_line:
                bar_command =  abjad.LilyPondLiteral(r'\bar "' + self.bar_line + '"', 'before')
                abjad.attach(bar_command, music_start)

    # TO DO: this is experimental only at the moment...
    def free_box(self, arrows=0, **kwargs):
        return_bubble = copy(self)
        return_bubble.commands = [c for c in self.commands]
        return_bubble.commands.append( ("freeOn", "before") )
        # return_bubble.commands.append( ("leftBracket", "before") )
        if not arrows:
            return_bubble.commands.append( ("freeAfter", "after") )
        return_bubble.commands.append( ("freeOff", "after") )
        return return_bubble


class SegmentMixin(object):
    """
    intended to be used with Fragment, SegmentMixin implements some conveniences useful for longer
    segments of music (e.g. adding rehearsal marks).
    """
    child_types = (Fragment, )
    tempo_text = None
    tempo_units_per_minute=None
    tempo_duration=(1,4) # only used if tempo_units_per_minute also specified
    tempo_command = None
    rehearsal_mark_number = None
    compress_full_bar_rests = None # TO DO... maybe this should be handled somewhere else? (currently it's being repeated where not necessary... at the beginning of every line)
    accidental_style = "modern-cautionary" # TO DO... necessary?

    def process_music(self, music, **kwargs):
        Fragment.process_music(self, music, **kwargs)
        if len(music) > 0:
            music_start = music[0]
            
            if self.rehearsal_mark_number:
                mark = abjad.RehearsalMark(number=self.rehearsal_mark_number)
                abjad.attach(mark, music_start)
            # NOTE... True adds command to compress, False adds compand to expand, None does nothing
            
            if self.compress_full_bar_rests == True:
                rests_command =  abjad.LilyPondLiteral(r"\compressFullBarRests", "before")
                abjad.attach(rests_command, music_start)

            elif self.compress_full_bar_rests == False:
                rests_command =  abjad.LilyPondLiteral(r"\expandFullBarRests", "before")
                abjad.attach(rests_command, music_start)

            # TO DO... TEMPO MAKES EVERYTHING SLOW... WHY?
            if self.tempo_text or self.tempo_units_per_minute:
                if self.tempo_units_per_minute:
                    tempo_reference_duration = Duration(self.tempo_duration)
                else:
                    tempo_reference_duration = None
                tempo = abjad.Tempo(tempo_reference_duration, units_per_minute=self.tempo_units_per_minute, textual_indication=self.tempo_text)
                abjad.attach(tempo, music_start)

            elif self.tempo_command:
                tempo_command =  abjad.LilyPondLiteral(r"\tempo \markup \fontsize #3 { %s }" % self.tempo_command, "before")
                # print(tempo_command)
                abjad.attach(tempo_command, music_start)

            if self.accidental_style:
                accidental_style_command = abjad.LilyPondLiteral(r"\accidentalStyle " + self.accidental_style, "before")
                abjad.attach(accidental_style_command, music_start)

class Segment(SegmentMixin, Fragment):
    pass

class MultiFragment(Fragment):
    """
    a fragment with temporary simultaneous music... optionally as multiple voices
    """
    multi_voiced = True
    is_simultaneous = True
    instruction = None

    def child_music(self, child_bubble):
        my_music = self.container_type()
        my_music.append( child_bubble.blow() )
        return my_music

    def music(self, **kwargs):
        # TO DO... test this!!!!!!
        my_music = super().music(**kwargs)

        if self.multi_voiced and len(my_music) > 1:
            for container in my_music[0:-1]:
                command_voices = abjad.LilyPondLiteral('\\ ', 'after')
                abjad.attach(command_voices, container)
            command_one_voice = abjad.LilyPondLiteral('\oneVoice', 'after')
            abjad.attach(command_one_voice, my_music)
        return my_music

class SimulFragment(MultiFragment):
    """
    same as MultiFragment, but defaults multi_voiced to False
    """
    multi_voiced = False

