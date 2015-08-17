from shutil import copyfile

from abjad import *

from settings import PROJECT_PATH

from .material import GLOBAL_MATERIAL, Material


class BubbleBase():
    name=None
    container_type=Container
    context_name=None
    is_simultaneous=False
    bubble_types = ()

    def make_callable(self, **kwargs):
        for attr_name in kwargs:
            attr = kwargs[attr_name] or getattr(self, attr_name)
            if attr is not None:
                if isinstance(attr, BubbleBase):
                    setattr(self, attr_name, attr.blow)
                elif isinstance(attr, Material):
                    setattr(self, attr_name, attr.get)
                elif callable(attr):
                    setattr(self, attr_name, attr)
                else:
                    setattr(self, attr_name, lambda : attr)


    # MAYBE TO DO... could be slick if all kwargs added to the bubble as attributes?
    def __init__(self, music=None, *args, **kwargs):
        self.make_callable(music=music)
        self.make_callable(sequence=None)

        # music = music or self.music
        # if music is not None:
        #     if isinstance(music, BubbleBase):
        #         self.music = music.blow
        #     elif isinstance(music, Material):
        #         self.music = music.get
        #     elif callable(music):
        #         self.music = music
        #     else:
        #         self.music = lambda : music 

    def music_container(self, *args, **kwargs):
        if self.is_simultaneous is not None:
            kwargs["is_simultaneous"] = self.is_simultaneous
        if self.context_name is not None:
            kwargs["context_name"] = self.context_name
        return self.container_type(*args, **kwargs)


    # IMPLEMENT IF NEEDED...
    # def before_music(self, music, *args, **kwargs):
    #     pass

    def music(self, *args, **kwargs):
        print("WARNING... EMPTY MUSIC FUNCTION CALLED ON BUBBLE BASE")
        return self.music_container()

    def before_music(self, music, *args, **kwargs):
        pass

    def after_music(self, music, *args, **kwargs):
        pass

    def blow(self, *args, **kwargs):
        # IMPLEMENT IF BEFORE_MUSIC NEEDED, OTHERWISE KISS
        # my_music = self.music_container()
        # self.before_music(my_music)
        # my_music.append(self.bubble_wrap().music())
        my_music = self.bubble_wrap().music()
        self.after_music(my_music)
        return my_music

    def bubble_wrap(self):
        return self

    def pdf_file_path(self):
        return PROJECT_PATH + "/pdf/" + type(self).__name__ + ".pdf"

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

    def show_pdf(self, music=None):
        """
        calls make_pdf and then shows the pdf: similar to abjad's builtin show() method... 
        but uses bubble-specific file path/name instead of the abjad default 
        and pdf filename does NOT increment
        """
        pdf_file_path = self.make_pdf(music)
        systemtools.IOManager.open_file(pdf_file_path)

    def __str__(self):
        music = self.blow()
        return(format(music))

class BubbleMaterial(Material, BubbleBase):

   def music(self, *args, **kwargs):
        my_music = self.music_container()
        my_music.append( self.get() )
        return my_music

class Placeholder(BubbleBase):
    sequence = ()

class Bubble(BubbleBase):
    is_simultaneous=True
    bubble_types = (BubbleBase,)

    def sequence(self, *args, **kwargs):
        # bubbles = [getattr(self,b) for b in dir(self) if isinstance(getattr(self,b), self.bubble_types)]
        # bubbles.sort(key=lambda x : x.order)
        seq_bubble = self.bubble_wrap()
        bubbles = [b for b in dir(seq_bubble) if isinstance(getattr(seq_bubble,b), self.bubble_types)]
        return bubbles

    @classmethod
    def blow_bubble(cls, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music
        """
        bubble = getattr(cls, bubble_name)
        if isinstance(bubble, Placeholder):
            bubble = cls.bubble_default()     
        # print(type(bubble.blow()))   
        return cls.bubble_imprint( bubble.blow() )

    @classmethod
    def bubble_imprint(cls, music):
        return music

    @classmethod
    def bubble_default(cls):
        return Bubble()

    def music(self, *args, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
               append_music = type(self).blow_bubble(bubble_name)
               my_music.append(append_music)
        return my_music


    def score(self, *args, **kwargs):
        """
        a quick way to get a full-fledged ajad score object for this bubble type...
        """
        score = Score()
        # TO DO... ADD SCORE TITLE (THE NAME OF THE CLASS)
        # RE-ADD IF BEFORE_MUSIC NEEDED...`
        # try:
        #     self.before_music(score, *args, **kwargs)
        # except:
        #     print("WARNING: error trying to run 'before_music' on the auto-generated score. Some music may be missing...")

        def append_staff(name, bubble):
            staff = Staff(name=name)
            staff.append( bubble.blow() )
            instrument = instrumenttools.Instrument(instrument_name=name, short_instrument_name=name)
            attach(instrument, staff)
            score.append(staff)            

        if self.is_simultaneous:
            for i, b in enumerate(self.sequence()):
                bubble = Eval(type(self.bubble_wrap()), b)
                append_staff(b, bubble)
        else:
            append_staff(self.__class__.name, self)

        try:
            self.after_music(score, *args, **kwargs)
        except:
            print("WARNING: error trying to run 'after_music' on the auto-generated score. Some music may be missing...")

        return score


    def show(self, *args, **kwargs):
        score = self.score(*args, **kwargs)
        self.show_pdf(score)


class Eval(Bubble):
    def __init__(self, cls, bubble_name):
        self.is_simultaneous = getattr(cls, bubble_name).is_simultaneous
        super().__init__( lambda : cls.blow_bubble(bubble_name) )

class Line(Bubble):
    is_simultaneous = False

class GridSequence(Bubble):
    grid_sequence = ()

    @classmethod
    def blow_bubble(cls, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music.
        NOTE that classes that inherit from GridSequence should NOT override blow_bubble
        """
        bubble = getattr(cls, bubble_name)
        if isinstance(bubble, Placeholder):
            bubble = Sequence(bubble_name, bubble, cls.grid_sequence)
        return bubble.blow()

# QUESTION... Ok to inherit from placeholder here?
class Sequence(Placeholder):
    grid_sequence = ()

    def __init__(self, bubble_name, bubble, grid_sequence, *args, **kwargs):
        self.bubble_name = bubble_name
        self.container_type = bubble.container_type
        self.context_name = bubble.context_name
        self.grid_sequence = grid_sequence

    def music(self):
        my_music = self.music_container()
        for bubble_type in self.grid_sequence:
            my_music.append( bubble_type.blow_bubble(self.bubble_name) )
        return my_music


class BubbleWrap(Bubble):
    """
    a base class for bubbles that "wrap" other bubbles in order to modify or extend them (without going through the trouble
        of inheritence)
    """
    def __init__(self, bubble, *args, **kwargs):
        self.bubble_wrap = bubble.bubble_wrap
        self.is_simultaneous = bubble.is_simultaneous
        super().__init__(bubble, *args, **kwargs)

# class BubbleImprint(BubbleWrap):
#     def after_music(self, music):
#         pass

#     def imprint_bubble(self, bubble):


class BubbleWrapContainer(Bubble):
    """
    similar to bubble wrap, but a new container/bubble is created around the inner bubble
    """
    def __init__(self, music_bubble=None, instrument=None, *args, **kwargs):
        self.music_bubble = lambda : music_bubble
        super().__init__(*args, **kwargs)

    def music(self, *args, **kwargs):
        my_music = self.music_container()
        bubble = self.music_bubble()
        if isinstance(bubble, BubbleBase): # just as a precaution
            my_music.append( bubble.blow() )
        return my_music

class Transpose(BubbleWrap):
    def __init__(self, bubble, transpose_expr, *args, **kwargs):
        self.transpose_expr = transpose_expr
        super().__init__(bubble, *args, **kwargs)
    
    def after_music(self, music, *args, **kwargs):
        super().after_music(music, *args, **kwargs)
        mutate(music).transpose(self.transpose_expr)

class BubbleStaff(BubbleWrapContainer):
    is_simultaneous = None
    container_type = Staff

    def __init__(self, music_bubble=None, instrument=None, clef=None, *args, **kwargs):
        self.instrument = instrument
        self.clef = clef
        super().__init__(music_bubble=music_bubble, *args, **kwargs)

    def after_music(self, music, *args, **kwargs):
        if self.instrument:
            attach(self.instrument, music)
        if self.clef:
            clef_obj = Clef(self.clef)
            attach(clef_obj, music)
        super().after_music(self, music)

    def show(self):
        self.show_pdf()

class BubbleRhythmicStaff(BubbleStaff):
    context_name="RhythmicStaff"

    def __init__(self, music_bubble=None, instrument=None, clef="percussion", *args, **kwargs):
        # TO DO ... why is the percussion clef showing up blank?????
        super().__init__(music_bubble=music_bubble, instrument=instrument, clef=clef, *args, **kwargs)

class BubbleGridMatch(Bubble):

    def __init__(self, grid_bubble=None, *args, **kwargs):
        self.grid_bubble = grid_bubble
        # set the grid bubble for any sub-bubbles (if not already defined) ... that way music bubbles passed to score
        # will be passed along to staff groups, and so on
        super().__init__(*args, **kwargs)
        self.set_grid_bubbles()

    def set_grid_bubbles(self):
        for bubble_name in self.sequence():
            bubble = getattr(self, bubble_name, None)
            if isinstance(bubble, BubbleGridMatch):
                bubble.grid_bubble = bubble.grid_bubble or self.grid_bubble
                BubbleGridMatch.set_grid_bubbles(bubble)

    def music(self, *args, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
                append_music = type(self).blow_bubble(bubble_name)
                if hasattr(self.grid_bubble, bubble_name):
                    append_music_inner = type(self.grid_bubble).blow_bubble(bubble_name)
                    append_music.append(append_music_inner)
                my_music.append(append_music)
        return my_music

class BubbleStaffGroup(BubbleGridMatch):
    is_simultaneous = None
    container_type = StaffGroup
    bubble_types=(BubbleStaff, BubbleGridMatch)

    def show(self):
        self.show_pdf()

class InstrumentStaffGroup(BubbleStaffGroup):

    def after_music(self, music):
        set_(music).systemStartDelimiter = "SystemStartSquare"

class BubbleScore(BubbleGridMatch):
    is_simultaneous = None
    container_type=Score
    bubble_types=(BubbleStaff, BubbleStaffGroup)

    # def __init__(self, music=None, *args, **kwargs):
    #     super().__init__(music, *args, **kwargs)
    #     if hasattr(self, "score_music"):

    def show(self):
        self.show_pdf()


class BubbleFormatLargeScore(BubbleScore):
    hide_empty = False
    title = None

    def after_music(self, music):
        super().after_music(self, music)
        music.add_final_bar_line()
        spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
        override(self).vertical_axis_group.staff_staff_spacing = spacing_vector
        override(self).staff_grouper.staff_staff_spacing = spacing_vector
        override(self).staff_symbol.thickness = 0.5
        set_(self).mark_formatter = schemetools.Scheme("format-mark-box-numbers")

    def show(self):
        music = self.get_lilypond_file()
        self.show_pdf(music)

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(music)

        # configure the lilypond file...
        lilypond_file.global_staff_size = 12

        if self.hide_empty:
            staff_context_block = lilypondfiletools.ContextBlock(
                source_context_name="Staff \\RemoveEmptyStaves",
                )
            rhythmic_staff_context_block = lilypondfiletools.ContextBlock(
                source_context_name="RhythmicStaff \\RemoveEmptyStaves",
                )
        else:
            staff_context_block = lilypondfiletools.ContextBlock()
            rhythmic_staff_context_block = lilypondfiletools.ContextBlock()

        override(staff_context_block).vertical_axis_group.remove_first = True
        lilypond_file.layout_block.items.append(staff_context_block)

        override(rhythmic_staff_context_block).vertical_axis_group.remove_first = True
        lilypond_file.layout_block.items.append(rhythmic_staff_context_block)

        slash_separator = indicatortools.LilyPondCommand('slashSeparator')
        lilypond_file.paper_block.system_separator_markup = slash_separator

        bottom_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        lilypond_file.paper_block.bottom_margin = bottom_margin

        top_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        lilypond_file.paper_block.top_margin = top_margin

        left_margin = lilypondfiletools.LilyPondDimension(0.75, 'in')
        lilypond_file.paper_block.left_margin = left_margin

        right_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
        lilypond_file.paper_block.right_margin = right_margin

        paper_width = lilypondfiletools.LilyPondDimension(11, 'in')
        lilypond_file.paper_block.paper_width = paper_width

        paper_height = lilypondfiletools.LilyPondDimension(17, 'in')
        lilypond_file.paper_block.paper_height = paper_height

        system_system_spacing = layouttools.make_spacing_vector(0, 0, 20, 0)
        lilypond_file.paper_block.system_system_spacing = system_system_spacing

        lilypond_file.header_block.composer = markuptools.Markup('Randall West')

        # TO DO... move "for Taiko and Orchestra" to subtitle
        lilypond_file.header_block.title = markuptools.Markup(self.title)
        # lilypond_file.header_block.tagline = markuptools.Markup(tagline)

        return lilypond_file