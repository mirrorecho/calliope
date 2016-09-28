import os,sys,inspect
from copy import copy, deepcopy
from shutil import copyfile
from abjad import * # get rid of this eventually (use import below instead)
import abjad
# from calliope._settings import PROJECT_PATH, ROOT_PATH # TO DO... GET RID OF THESE SETTINGS... SHOULD NOT BE NEEDED
from calliope.material import GLOBAL_MATERIAL
from calliope.tools import pitch 

PROJECT_PATH = "."

# TO DO... this is reduntant... remove
def illustrate_me_file(filename, module_path, illustrate_callable, subfolder=""):
    illustrate_me(module_path, illustrate_callable=illustrate_callable, filename=filename, subfolder=subfolder, open_pdf=False)

def illustrate_me(module_path, illustrate_callable, filename=None, subfolder="illustrations", as_pdf=True, open_pdf=True, as_midi=False):
    import __main__ as main
    if main.__file__ == module_path: # only conitnue if illustrate_me called from main (as opposed to imported module)
        module_name = os.path.split(module_path)[1].split(".")[0]
        illustration_directory_path = os.path.join(
            os.path.dirname(module_path),
            subfolder,
            )
        if not os.path.exists(illustration_directory_path):
            os.makedirs(illustration_directory_path)

        # NOTE... this is odd... within sublimetext using the virtual envionment package on a mac ONLY, 
        # lilypond executable is not founr properly (something to do with os.environ not finding the right PATH info)
        # ... adding this here solves as a quick-fix
        mac_default_lilypond_path = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
        if os.path.exists("/Applications/LilyPond.app/Contents/Resources/bin/lilypond"):
            from abjad import abjad_configuration
            abjad_configuration["lilypond_path"] = mac_default_lilypond_path

        my_persistance_agent = abjad.persist( illustrate_callable() )
        
        if as_pdf:
            pdf_filename = "%s.pdf" % (filename if filename is not None else module_name)
            illustration_file_path = os.path.join(
                illustration_directory_path,
                pdf_filename,
                )
            print(pdf_filename)
            print(illustration_file_path)

            my_persistance_agent.as_pdf(illustration_file_path)
            if open_pdf:
                abjad.systemtools.IOManager.open_file(illustration_file_path)
        if as_midi:
            pdf_filename = '%s.midi' % filename if filename is not None else module_name
            midi_file_path = os.path.join(
                illustration_directory_path,
                pdf_filename,
                )
            my_persistance_agent.as_midi(midi_file_path)

        # # TO DO... would be best to prevent abjad from re-illustrating, maybe something like below... 
        # # but also don't want to re-invent abjad's code here:
        # ly_file_path, abjad_time = my_persistance_agent.as_ly(illustration_file_path)
        # timer = abjad.systemtools.Timer()
        # with timer:
        #     success = systemtools.IOManager.run_lilypond(ly_file_path)
        # abjad.systemtools.IOManager.open_file(illustration_file_path)


class BubbleBase(object):
    name=None
    container_type=Container
    context_name=None
    is_simultaneous=False
    bubble_types = ()
    commands = ()
    sequence = ()
    respell=None # TO DO, best place for this?
    process_methods = ()
    stylesheets = None

    def make_callable(self, attr_name):
        attr = getattr(self, attr_name, None)
        if attr is not None:
            if isinstance(attr, BubbleBase):
                setattr(self, attr_name, attr.blow)
            # elif isinstance(attr, Material):
            #     setattr(self, attr_name, attr.get)
            elif callable(attr):
                setattr(self, attr_name, attr)
            else:
                setattr(self, attr_name, lambda : attr)

    def __init__(self, **kwargs):
        # the first arg is always the music, if passed:
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.make_callable("music")
        self.make_callable("sequence")
        self.setup()
        self.arrange()

    def setup(self, **kwargs):
        """
        hook that's called at end of bubble __init__ method (just before arrange), 
        for adjusting bubble atributes / actual bubble material, etc.
        """
        pass

    def arrange(self, **kwargs):
        """
        hook that's called at end of bubble __init__ method, for arranging music
        (usually dealing with bubble attributes... adding articulations, phrasing, etc.)
        """
        pass

    # TO DO... depreciate...
    def latch(self, **kwargs):
        return_bubble = copy(self)
        for name, value in kwargs.items():
            setattr(return_bubble, name, value)
        return return_bubble

    # def process(self, method, *args, **kwargs):
    #     return_bubble = copy(self)
    #     return_bubble.process_methods = copy(self.process_methods)
    #     return_bubble.process_methods.append(lambda music: method(music, *args, **kwargs))
    #     return return_bubble

    def music_container(self, **kwargs):
        if self.is_simultaneous is not None:
            kwargs["is_simultaneous"] = self.is_simultaneous
        if self.context_name is not None:
            kwargs["context_name"] = self.context_name
        return self.container_type(name=self.name, **kwargs)

    def music(self, **kwargs):
        self.warn("empty music method called on bubble base... music method needs to be overriden somewhere")
        return self.music_container()

    # clever... need to test this carefully!
    def __add__(self, other):
        return BubbleSequence( bubbles=(self, other) )

    def __mul__(self, num):
        return BubbleSequence( bubbles = [self for i in range(num)] )
    
    # IMPLEMENT IF NEEDED...
    # def before_music(self, music, **kwargs):
    #     pass

    def after_music(self, music, **kwargs):
        # TO DO... is this the best place for respell, etc.?
        if self.respell:
            pitch.respell(music, self.respell)
        # TO DO... look at these process_methods in light of "machines" work in copper
        for m in self.process_methods:
            m(music)

    def blow(self, **kwargs):
        
        # IMPLEMENT IF BEFORE_MUSIC NEEDED, OTHERWISE KISS
        # my_music = self.music_container()
        # self.before_music(my_music)
        # my_music.append(self.bubble_wrap().music())

        my_music = self.bubble_wrap().music()
        self.after_music(my_music)
        for c in self.commands:
            command = indicatortools.LilyPondCommand(c[0], c[1])
            attach(command, my_music)
        return my_music

    def bubble_wrap(self):
        return self

    def pdf_file_path(self):
        return PROJECT_PATH + "/pdf/" + type(self).__name__ + ".pdf"

    def ly_file_path(self):
        return PROJECT_PATH + "/ly/" + type(self).__name__ + ".ly"

    def play(self, music=None):
        music = music or self.blow()
        play(music)

    def make_pdf(self, music=None):
        music = music or self.blow()
        assert '__illustrate__' in dir(music)
        result = topleveltools.persist(music).as_pdf()
        abjad_pdf_file_path = result[0]
        abjad_formatting_time = result[1]
        lilypond_rendering_time = result[2]
        success = result[3]
        if success:
            # not sure why save_last_pdf_as doesn't work (UnicodeDecodeError)... so just using copyfile instead
            #systemtools.IOManager.save_last_pdf_as(project_pdf_file_path)
            pdf_file_path = self.pdf_file_path()
            copyfile(abjad_pdf_file_path, pdf_file_path)
            return pdf_file_path
        # if return_timing:
        #     return abjad_formatting_time, lilypond_rendering_time

    # def __illustrate__(self):
    #     r'''Illustrates component.

    #     Returns LilyPond file.
    #     '''
    #     from abjad.tools import lilypondfiletools
    #     music = music or self.blow()
    #     assert '__illustrate__' in dir(music)
    #     lilypond_file = lilypondfiletools.make_basic_lilypond_file(music)
    #     lilypond_file.header_block.tagline = False
    #     return lilypond_file

    def show_pdf(self, music=None):
        """
        calls make_pdf and then shows the pdf: similar to abjad's builtin show() method... 
        but uses bubble-specific file path/name instead of the abjad default 
        and pdf filename does NOT increment
        """
        pdf_file_path = self.make_pdf(music)
        systemtools.IOManager.open_file(pdf_file_path)

    def save(self):
        music = self.blow()
        with open(self.ly_file_path(), "w") as ly_file:
            ly_file.write(format(music))

    def warn(self, msg, data=None, **kwargs):
        print("WARNING - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def info(self, msg, data=None, **kwargs):
        print("INFO - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def verify(self, condition, msg=None, data=None, **kwargs):
        if not condition:
            self.warn(msg or "(no message)", data)
        return condition

    def __str__(self):
        music = self.blow()
        return(format(music))


class Placeholder(BubbleBase):
    sequence = ()

class Bubble(BubbleBase):
    is_simultaneous=True
    bubble_types = (BubbleBase,)

    def sequence(self, **kwargs):
        # bubbles = [getattr(self,b) for b in dir(self) if isinstance(getattr(self,b), self.bubble_types)]
        # bubbles.sort(key=lambda x : x.order)
        seq_bubble = self.bubble_wrap()
        bubbles = [b for b in dir(seq_bubble) if isinstance(getattr(seq_bubble,b), self.bubble_types)]
        return bubbles

    def blow_bubble(self, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music
        """
        bubble = getattr(self, bubble_name)
        if isinstance(bubble, Placeholder) and hasattr(self, "bubble_default"):
            bubble = self.bubble_default   
        # print(type(bubble.blow()))   
        return self.bubble_imprint( bubble.blow() )

    def bubble_imprint(self, music):
        return music

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
               append_music = self.blow_bubble(bubble_name)
               my_music.append(append_music)
        return my_music


    def score(self, **kwargs):
        """
        a quick way to get a full-fledged ajad score object for this bubble type...
        """
        # TO DO... refactor to use BubbleScore
        score = Score()
        # TO DO... ADD SCORE TITLE (THE NAME OF THE CLASS)
        # RE-ADD IF BEFORE_MUSIC NEEDED...`
        # try:
        #     self.before_music(score, **kwargs)
        # except:
        #     print("WARNING: error trying to run 'before_music' on the auto-generated score. Some music may be missing...")

        def append_staff(name, bubble=None, bubble_name=None):
            staff = Staff(name=name)
            music = bubble.blow() if bubble is not None else self.blow_bubble(bubble_name)
            staff.append( music )
            instrument = instrumenttools.Instrument(instrument_name=name, short_instrument_name=name)
            attach(instrument, staff)
            score.append(staff)

        if self.is_simultaneous:
            for b in self.sequence():
                append_staff(b, bubble=None, bubble_name=b)
        else:
            append_staff(self.__class__.name, bubble=self)

        try:
            self.after_music(score, **kwargs)
        except:
            self.warn("error trying to run 'after_music' on the auto-generated score. Some music may be missing...")

        # TO DO... refactor to use BubbleScore
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score, includes=self.stylesheets)
        # include_command = indicatortools.LilyPondCommand("', 'before')
        # print(include_command)
        # attach(include_command, lilypond_file.paper_block)
        # lilypond_file.items.insert(3, '\\include "' + ROOT_PATH + '/calliope/ly_includes/ametric.ly"')

        # print(format(lilypond_file))

        return lilypond_file


    def show(self, **kwargs):
        score = self.score(**kwargs)
        self.show_pdf(score)

# TO DO... this shouldn't be necessary...?
# class Eval(Bubble):
#     def __init__(self, cls, bubble_name):
#         self.is_simultaneous = getattr(cls, bubble_name).is_simultaneous
#         super().__init__( music = lambda : cls.blow_bubble(bubble_name) )

class LineAttachments:
    show_indices = False
    dynamics = ()
    slurs = ()
    endos = ()
    instructions = ()    

class Line(Bubble):
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
    

    def __init__(self, music_string=None, **kwargs):
        """
        overriding __init__ simply to be able to use music_string as a positional argument
        """
        if music_string:
            self.music_string = music_string
        super().__init__(**kwargs)

    def __add__(self, other):
        return LineSequence( bubbles=(self, other) )

    def __mul__(self, num):
        return LineSequence( bubbles = [self for i in range(num)] )

    def music(self, **kwargs):
        if self.music_string:
            my_music = self.container_type( self.music_string )
            # self.container_type = type(my_music) # TO DO: necessary?
            self.is_simultaneous = my_music.is_simultaneous # TO DO: necessary?
            return my_music
        else:
            return super().music(**kwargs)

    def after_music(self, music, **kwargs):
        if len(music) > 0:
            music_start = music[0]

            if self.transpose:
                mutate(music).transpose(self.transpose)

            if self.time_signature:
                # TO DO... is the numeric commad necessary... maybe just include it at the score level?
                time_command_numeric =  indicatortools.LilyPondCommand("numericTimeSignature", "before")
                attach(time_command_numeric, music_start)

                time_command =  indicatortools.LilyPondCommand("time " + str(self.time_signature[0]) + "/" + str(self.time_signature[1]), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                attach(time_command, music)
            if self.clef:
                clef_obj = Clef(self.clef)
                attach(clef_obj, music_start)
            if self.start_bar_line:
                bar_command =  indicatortools.LilyPondCommand('bar "' + self.start_bar_line + '"', 'before')
                attach(bar_command, music_start)
            if self.rehearsal_mark_number:
                mark = indicatortools.RehearsalMark(number=self.rehearsal_mark_number)
                attach(mark, music_start)
            # NOTE... True adds command to compress, False adds compand to expand, None does nothing
            if self.compress_full_bar_rests == True:
                rests_command =  indicatortools.LilyPondCommand("compressFullBarRests", "before")
                attach(rests_command, music_start)
            elif self.compress_full_bar_rests == False:
                rests_command =  indicatortools.LilyPondCommand("expandFullBarRests", "before")
                attach(rests_command, music_start)

            # TO DO... TEMPO MAKES EVERYTHING SLOW... WHY?
            if self.tempo_text or self.tempo_units_per_minute:
                if self.tempo_units_per_minute:
                    tempo_reference_duration = Duration(self.tempo_duration)
                else:
                    tempo_reference_duration = None
                tempo = indicatortools.Tempo(tempo_reference_duration, units_per_minute=self.tempo_units_per_minute, textual_indication=self.tempo_text)
                attach(tempo, music_start)
            elif self.tempo_command:
                tempo_command =  indicatortools.LilyPondCommand("tempo \markup \\fontsize #3 { %s }" % self.tempo_command, "before")
                # print(tempo_command)
                attach(tempo_command, music_start)


            if self.accidental_style:
                accidental_style_command = indicatortools.LilyPondCommand("accidentalStyle " + self.accidental_style, "before")
                attach(accidental_style_command, music_start)
            super().after_music(music, **kwargs)

    def free_box(self, arrows=0, **kwargs):
        return_bubble = copy(self)
        return_bubble.commands = [c for c in self.commands]
        return_bubble.commands.append( ("freeOn", "before") )
        # return_bubble.commands.append( ("leftBracket", "before") )
        if not arrows:
            return_bubble.commands.append( ("freeAfter", "after") )
        return_bubble.commands.append( ("freeOff", "after") )
        return return_bubble


class Ly(Line):
    ly_material = None # the name of material to load

    def __init__(self, ly_material=None, **kwargs):
        self.ly_material = ly_material or self.ly_material
        super().__init__(music_string=self.get_ly_material(), **kwargs)

    def get_ly_material(self):
        search_list = self.ly_material.split(".")
        material_name = search_list[0]
        material_var = search_list[1]

        GLOBAL_MATERIAL.use(material_name)
        
        ly_string = GLOBAL_MATERIAL[material_name].get(material_var, None)

        if not ly_string:
            print("WARNING: '" + material_var + "' variable does not exist in the material file: '" + material_name + ".ly'")

        return ly_string


class MultiLine(Line):
    """
    a line with temporary simultaneous music... optionally as multiple voices
    """
    multi_voiced = True
    is_simultaneous = True
    instruction = None

    def bubble_imprint(self, music):
        my_music = Container()
        my_music.append(music)
        return my_music

    def music(self, **kwargs):
        my_music = super().music(**kwargs)

        if self.multi_voiced and len(my_music) > 1:
            for container in my_music[0:-1]:
                command_voices = indicatortools.LilyPondCommand('\\ ', 'after')
                attach(command_voices, container)
            command_one_voice = indicatortools.LilyPondCommand('oneVoice', 'after')
            attach(command_one_voice, my_music)
        return my_music

class SimulLine(MultiLine):
    """
    same as MultiLine, but defaults multi_voiced to False
    """
    multi_voiced = False

class LineLyrics(Line):
    lyrics = ""

# TO DO... this be specified at the line level!!!!!!!!!!!!!!!!!!
class Ametric(Bubble):
    show_x_meter = False
    show_time_span = False
    start_text = None # e.g. "Freely"
    time_span_text = None # e.g. "10'' ca"
    duration = (2,1)
    start_bar_line = "!"
    end_bar_line = None
    accidental_style = None

    def blow_bubble(self, bubble_name):
        """
        overriding blow_bubble to add free stuff to each sub-bubble
        """
        music = super().blow_bubble(bubble_name)
        
        # this will auto-increase the length of the music (in skips) to the length of the Ametric duration
        add_skips_duration = Duration(self.duration) - inspect_(music).get_duration()
        if add_skips_duration > 0:
            skips = scoretools.make_skips( Duration(1, add_skips_duration.denominator), ((add_skips_duration.numerator,add_skips_duration.denominator),) )
            music.append(skips)

        leaves = select(music).by_leaf()
        if self.show_x_meter:
            x_meter_command = indicatortools.LilyPondCommand( ("timeX"), "before" )
            attach(x_meter_command, music)
        else:
            # HIDE THE TIME SIGNATURE:
            hide_time_command = indicatortools.LilyPondCommand("""once \override Staff.TimeSignature #'stencil = ##f """, "before")
            attach(hide_time_command, music)
        if self.duration:
            time_command =  indicatortools.LilyPondCommand("time " + str(self.duration[0]) + "/" + str(self.duration[1]), "before")
            attach(time_command, music)
        if self.start_bar_line:
            bar_command =  indicatortools.LilyPondCommand('bar "' + self.start_bar_line + '"', 'before')
            attach(bar_command, music)
        else:
            # MAYBE TO DO... auto calculate bar-length based on longest bubble
            pass
        if self.start_text or self.time_span_text:
            # TO DO... this could conflict with tempo mark / text
            # ALSO MAYBE TO DO... better time_span_text using a measure-length spanner
            my_text = ", ".join([t for t in [self.start_text, " " + self.time_span_text] if t])
            tempo_text = indicatortools.Tempo(textual_indication=my_text)
            attach(tempo_text, music)
        if self.accidental_style:
            accidental_style_command = indicatortools.LilyPondCommand("accidentalStyle " + self.accidental_style, "before")
            attach(accidental_style_command, music)
        return music

class AmetricStart(Ametric):
    start_bar_line = "||"
    show_x_meter = True
    start_text = "Freely"
    accidental_style = "neo-modern-cautionary"

class GridSequence(Bubble):
    grid_sequence = ()

    def blow_bubble(self, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music.
        NOTE that classes that inherit from GridSequence should NOT override blow_bubble
        """
        bubble = getattr(self, bubble_name)
        if isinstance(bubble, Placeholder):
            bubble = Sequence(
                bubble_name=bubble_name, 
                container_type = bubble.container_type,
                context_name = bubble.context_name,
                grid_sequence=self.grid_sequence)
        return bubble.blow()

# QUESTION... Ok to inherit from placeholder here?
class Sequence(Placeholder):
    grid_sequence = ()
    lyrics = None
    bubble_name = None

    def music(self):
        my_music = self.music_container()
        # has_lyrics = False
        # my_lyrics = ""
        for bubble in self.grid_sequence:
            my_music.append( bubble.blow_bubble(self.bubble_name) )
            # TO DO... any way to encapsulate this better so that it's not part of EVERY sequence?
            # PLUS, is it odd to do this in the music method?
        #     if hasattr( getattr(bubble_type, self.bubble_name), "lyrics"):
        #         has_lyrics = True
        #         my_lyrics += getattr(bubble_type, self.bubble_name).lyrics + " "
        # if has_lyrics:
        #     print("BAAAHHH............")
        #     self.lyrics = my_lyrics
        return my_music

    # TO DO... any way to encapsulate this better so that it's not part of EVERY sequence?
    # def after_music(self, music, **kwargs):
    #     has_lyrics = False
    #     my_lyrics = ""
    #     for bubble_type in self.grid_sequence:
    #         if hasattr( getattr(bubble_type, self.bubble_name), "lyrics"):
    #             has_lyrics = True
    #             my_lyrics += getattr(bubble_type, self.bubble_name).lyrics + " "
    #     if has_lyrics:
    #         self.lyrics = my_lyrics
    #         lyrics_command = indicatortools.LilyPondCommand("addlyrics { " + self.lyrics + " }", "after")
    #         attach(lyrics_command, music)
    #     super().after_music(self, music, **kwargs)


# TO DO... naming is confusing in combo with the above classes..
# ... also, should rethink sequencing more universally... 
class BubbleSequence(Bubble):
    bubbles = ()
    is_simultaneous = False

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble in self.bubbles:
            my_music.append(bubble.blow())
        return my_music

class LineSequence(BubbleSequence, Line):
    pass

class BubbleWrap(Bubble):
    """
    a base class for bubbles that "wrap" other bubbles in order to modify or extend them 
    (without going through the trouble of inheritence)
    """
    def __init__(self, bubble, **kwargs):
        self.bubble_wrap = bubble.bubble_wrap
        self.is_simultaneous = bubble.is_simultaneous
        super().__init__(**kwargs)


class BubbleWrapContainer(Bubble):
    """
    similar to bubble wrap, but a new container/bubble is created around the inner bubble
    """
    def __init__(self, music_bubble=None, **kwargs):
        self.music_bubble = lambda : music_bubble
        super().__init__(**kwargs)

    def music(self, **kwargs):
        my_music = self.music_container()
        bubble = self.music_bubble()
        if isinstance(bubble, BubbleBase): # just as a precaution
            # if hasattr(bubble, "lyrics"):
            #     print("BOOOOOOOOOOOOOOOOO")
            my_music.append( bubble.blow() )
        return my_music

   # TO DO... any way to encapsulate this better so that it's not part of EVERY bubble wrap container?
    # def after_music(self, music, **kwargs):
    #     bubble = self.music_bubble()
    #     if isinstance(bubble, BubbleBase):
    #         print(bubble )
    #         if hasattr(bubble, "lyrics"):
    #             print("BOOOOOOOOOOOOOOOOO")
    #             lyrics_command = indicatortools.LilyPondCommand("addlyrics { " + bubble.lyrics + " }", "after")
    #             attach(lyrics_command, music)
    #     super().after_music(self, music, **kwargs)

# TO DO... depreciate:
class Transpose(BubbleWrap):
    transpose_expr = 0
    
    def after_music(self, music, **kwargs):
        mutate(music).transpose(self.transpose_expr)
        super().after_music(music, **kwargs)

class Tr(Transpose):
    """
    just a shortcut for the Transpose class, since it's used often enough ...
    """
    def __init__(self, bubble, transpose_expr, **kwargs):
        super().__init__(bubble=bubble, transpose_expr=transpose_expr, **kwargs)



class BubbleVoice(BubbleWrapContainer):
    is_simultaneous = None
    container_type = Voice


class BubbleStaff(BubbleWrapContainer):
    is_simultaneous = None
    container_type = Staff
    instrument = None
    clef = None

    def after_music(self, music, **kwargs):
        if self.instrument:
            attach(self.instrument, music)
        if self.clef:
            clef_obj = Clef(self.clef)
            attach(clef_obj, music)
        super().after_music(music, **kwargs)

    def show(self):
        self.show_pdf()

class BubbleRhythmicStaff(BubbleStaff):
    context_name="RhythmicStaff"
    clef="percussion"


# maybe bubble grid match should be applicable for all bubbles???
class BubbleGridMatch(Bubble):
    grid_bubble=None

    def __init__(self, grid_bubble=None, **kwargs):
        # set the grid bubble for any sub-bubbles (if not already defined) ... that way music bubbles passed to score
        # will be passed along to staff groups, and so on
        if grid_bubble:
            self.grid_bubble = grid_bubble
        super().__init__(**kwargs)
        self.set_grid_bubbles()

    def set_grid_bubbles(self):
        for bubble_name in self.sequence():
            bubble = getattr(self, bubble_name, None)
            if isinstance(bubble, BubbleGridMatch):
                bubble.grid_bubble = bubble.grid_bubble or self.grid_bubble
                BubbleGridMatch.set_grid_bubbles(bubble)

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
                append_music = self.blow_bubble(bubble_name)
                if hasattr(self.grid_bubble, bubble_name):
                    append_music_inner = self.grid_bubble.blow_bubble(bubble_name)
                    append_music.append(append_music_inner)
                my_music.append(append_music)
        return my_music

class BubbleStaffGroup(BubbleGridMatch):
    is_simultaneous = None
    container_type = StaffGroup
    bubble_types=(BubbleStaff, BubbleGridMatch)
    instrument = None
    
    def after_music(self, music, **kwargs):
        if self.instrument:
            attach(self.instrument, music)
        super().after_music(music, **kwargs)

    def show(self):
        self.show_pdf()

class BubblePiano(BubbleStaffGroup):
    piano1 = BubbleStaff()
    piano2 = BubbleStaff(clef="bass")
    context_name = "PianoStaff"
    sequence = ("piano1", "piano2")
    instrument=instrumenttools.Piano()

class BubbleHarp(BubbleStaffGroup):
    harp1 = BubbleStaff()
    harp2 = BubbleStaff(clef="bass")
    context_name = "PianoStaff"
    sequence = ("harp1", "harp2")
    instrument=instrumenttools.Harp()

class BubbleGridStaff(BubbleGridMatch, BubbleStaff):
    """
    creates a staff with a voice or voices inside of it
    """
    bubble_types=(BubbleVoice) # needed? (throws exception otherwise... why?)
    instrument=None
    clef=None

class InstrumentStaffGroup(BubbleStaffGroup):
    def after_music(self, music, **kwargs):
        super().after_music(music, **kwargs)
        set_(music).systemStartDelimiter = "SystemStartSquare"

class BubbleScore(BubbleGridMatch):
    is_simultaneous = None
    container_type=Score
    hide_empty = False # TO DO... this is currently not longer used... keep it?
    bubble_types=(BubbleStaff, BubbleStaffGroup)
    global_staff_size = None
    staff_context_block = None
    rhythmic_staff_context_block = None
    title = ""

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(music, includes=self.stylesheets, 
            # global_staff_size=self.global_staff_size
            )

        # configure the lilypond file...
        # lilypond_file.global_staff_size = 12

        # THIS IS NOW CONTROLLED THROUGH THE STYLESHEETS
        # if self.hide_empty:
        #     self.staff_context_block = lilypondfiletools.ContextBlock(
        #         source_context_name="Staff \\RemoveEmptyStaves",
        #         )
        #     self.rhythmic_staff_context_block = lilypondfiletools.ContextBlock(
        #         source_context_name="RhythmicStaff \\RemoveEmptyStaves",
        #         )
        # else:
        #     self.staff_context_block = lilypondfiletools.ContextBlock()
        #     self.rhythmic_staff_context_block = lilypondfiletools.ContextBlock()

        # override(staff_context_block).vertical_axis_group.remove_first = True
        # lilypond_file.layout_block.items.append(self.staff_context_block)

        # override(rhythmic_staff_context_block).vertical_axis_group.remove_first = True
        # lilypond_file.layout_block.items.append(self.rhythmic_staff_context_block)

        # lilypond_file.header_block.composer = markuptools.Markup('Randall West')

        # TO DO... move "for Taiko and Orchestra" to subtitle
        # lilypond_file.header_block.title = markuptools.Markup(self.title)
        # lilypond_file.header_block.tagline = markuptools.Markup("")
        self.info("got abjad representation of lilypond file... now rendering with lilypond")
        return lilypond_file

    def after_music(self, music, **kwargs):
        super().after_music(music, **kwargs)
        music.add_final_bar_line()
        self.info("finished creating abjad music container object for the score")

    def show(self):
        music = self.get_lilypond_file()
        # print(music)
        self.show_pdf(music)

    # def make_pdf(self, music):
        # music = self.get_lilypond_file()
        # super().make_pdf(music)        

    def save(self):
        music = self.get_lilypond_file()
        with open(self.ly_file_path(), "w") as ly_file:
            ly_file.write(format(music))

    def __str__(self):
        music = self.get_lilypond_file()
        return(format(music))


class BubbleFormatLargeScore(BubbleScore):
    global_staff_size = 16

    def after_music(self, music, **kwargs):
        super().after_music(music, **kwargs)
        # spacing_vector = schemetools.make_spacing_vector(0, 0, 8, 0)
        # override(self).vertical_axis_group.staff_staff_spacing = spacing_vector
        # override(self).staff_grouper.staff_staff_spacing = spacing_vector
        # override(self).staff_symbol.thickness = 0.5
        # set_(self).mark_formatter = schemetools.Scheme("format-mark-box-numbers")


    def get_lilypond_file(self):
        lilypond_file = super().get_lilypond_file()
        # configure the lilypond file...

        # override(self.staff_context_block).vertical_axis_group.remove_first = True
        # lilypond_file.layout_block.items.append(self.staff_context_block)

        # override(self.rhythmic_staff_context_block).vertical_axis_group.remove_first = True
        # lilypond_file.layout_block.items.append(self.rhythmic_staff_context_block)

        # slash_separator = indicatortools.LilyPondCommand('slashSeparator')
        # lilypond_file.paper_block.system_separator_markup = slash_separator

        # bottom_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        # lilypond_file.paper_block.bottom_margin = bottom_margin

        # top_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        # lilypond_file.paper_block.top_margin = top_margin

        # left_margin = lilypondfiletools.LilyPondDimension(0.75, 'in')
        # lilypond_file.paper_block.left_margin = left_margin

        # right_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        # lilypond_file.paper_block.right_margin = right_margin

        # paper_width = lilypondfiletools.LilyPondDimension(11, 'in')
        # lilypond_file.paper_block.paper_width = paper_width

        # paper_height = lilypondfiletools.LilyPondDimension(17, 'in')
        # lilypond_file.paper_block.paper_height = paper_height

        # system_system_spacing = schemetools.make_spacing_vector(0, 0, 20, 0)
        # lilypond_file.paper_block.system_system_spacing = system_system_spacing

        # lilypond_file.header_block.composer = markuptools.Markup('Randall West')

        # TO DO... move "for Taiko and Orchestra" to subtitle
        # lilypond_file.header_block.title = markuptools.Markup(self.title)
        # lilypond_file.header_block.tagline = markuptools.Markup(tagline)

        return lilypond_file

