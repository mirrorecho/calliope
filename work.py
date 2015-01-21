from abjad import *
from collections import OrderedDict
from shutil import copyfile

from calliope.settings import *

class Project():
    def __init__(self, name, title="", output_path=OUTPUT_PATH):
        self.name = name
        self.output_path = output_path
        self.project_path = output_path + "/" + name
        self.pdf_path = self.project_path + "/" + PDF_SUBFOLDER
        self.data_path = self.project_path + "/" + DATA_SUBFOLDER

## MAYBE THIS SHOULD INHERIT FROM STAFF...??!
class Part(Staff):

    def __init__(self, name, instrument=None, clef=None, context_name='Staff'):
        super().__init__(name=name, context_name=context_name) # why doesn't context name work?

        # these attribbutes even needed?
        self.instrument = instrument 
        self.context_name = context_name # TO DO... understand what these contexts are doing
        self.name = name
        self.start_clef = clef

        attach(self.instrument, self)
        
        if clef is not None:
            attach(Clef(name=clef), self)


    def make_staff(self):
        return self

class PercussionPart(Part):
    def __init__(self, name, instrument=None, clef=None):
        super().__init__(name, instrument, clef, 'RhythmicStaff')

    
    # def make_staff(self):
    #     # question... what about hi/low type of things... better to explicitly specify number of staff lines? 
    #     staff = scoretools.Staff([], context_name='RhythmicStaff')
    #     attach(self.instrument, staff)
    #     staff.extend(self)
    #     return staff

class PianoStaffPart(Part):

    def __init__(self, name, instrument=None):
        super().__init__(name=name, instrument=instrument)
        self.is_simultaneous = True
        self.append(scoretools.Container()) # music for top staff
        self.append(scoretools.Container()) # music for bottom staff

    def make_staff(self):
        staff_group = StaffGroup()
        staff_group.context_name = 'PianoStaff' # should the context name always be piano staff??
        staff_group.append(Staff([]))
        staff_group.append(Staff([]))

        attach(self.instrument, staff_group)

        # should we always attach this clef here?
        attach(Clef(name='bass'), staff_group[1])

        staff_group[0].extend(self[0])
        staff_group[1].extend(self[1])

        return staff_group

class Arrangement:
    """
    Represents a collection of parts. Parts should be added in score order.
    """

    # TO DOs:
    # - get/set length?
    # - option to hide empty parts/staves
    # - fill parts with rests/skips
    # - arrange at certain duration
    # - specify paper/book/misc lilypond output settings


    def __init__(self, name="full-score", project=None, title="Full Score", layout="standard", time_signature=TimeSignature( (4,4) ) ):
        self.parts = OrderedDict()
        self.score = scoretools.Score([])
        self.output_path = OUTPUT_PATH
        self.layout = layout
        if project is not None:
            self.project = project
        else:
            self.project = Project("rwestmusic")
        self.title = title
        self.time_signature = time_signature
        self.name = name

        # right now this is being used to deterimne the length (i.e. to fil with rests)
        # ... some better way to handle?
        self.empty_measures = Container("R1 " * 8)

        # useful for building up little rhythmic phrases and then arranging them by passing a list of names
        self.rhythms = {}

        # similarly, for building up 
        self.pitch_material = {}

    def arrange_music(self, part_names, rhythms=[], rhythm_strings=[], pitch_material=[None], respell_sets=[None], transpose_sets=[0]):
        for i, part_name in enumerate(part_names):
            pitches = pitch_sets[i % len(pitch_sets)]
            durations = duration_sets[i % len(duration_sets)]
            respell = respell_sets[i % len(respell_sets)]
            transpose=transpose_sets[i % len(transpose_sets)]

            # TO DO... could pass along split durations here...
            self.parts[part_name].extend(music_from_durations(durations=durations, pitches=pitches, transpose=transpose, respell=respell))

    def fill_empty_parts_with_rests(self):
        for part_name in self.parts:
            if len(self.parts[part_name]) == 0:
                self.parts[part_name].extend(copy.deepcopy(self.empty_measures))

    def pdf_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.pdf_path + "/" + subfolder + self.project.name + "-" + self.name + ".pdf"

    def add_part(self, name, instrument=None, clef=None):
        self.parts[name] = Part(name=name, instrument=instrument, clef=clef)

    def add_perc_part(self, name, instrument=None):
        self.parts[name] = PercussionPart(name=name, instrument=instrument)

    def add_piano_staff_part(self, name, instrument=None):
        self.parts[name] = PianoStaffPart(name=name, instrument=instrument)

    def make_score(self, part_names = None):

        self.score = scoretools.Score([])

        if part_names is None:
            part_names = self.parts

        for p in part_names:
            # NOTE / QUESTION... will this work for piano/multi staff parts...?
            part_staff = self.parts[p].make_staff()
            attach(self.time_signature, part_staff)
            self.score.append(part_staff)

    def make_lilypond_file(self):
        """
        Makes Lilypond File
        """
        if self.layout == "standard":
            #configure the score ... 
            # spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
            # override(self.score).vertical_axis_group.staff_staff_spacing = spacing_vector
            # override(self.score).staff_grouper.staff_staff_spacing = spacing_vector
            set_(self.score).mark_formatter = schemetools.Scheme('format-mark-box-numbers')
            lilypond_file = lilypondfiletools.make_basic_lilypond_file(self.score)

            # configure the lilypond file...
            lilypond_file.global_staff_size = 16

            context_block = lilypondfiletools.ContextBlock(
                source_context_name="Staff \RemoveEmptyStaves",
                )
            override(context_block).vertical_axis_group.remove_first = True
            lilypond_file.layout_block.items.append(context_block)

            # assume we can use default dimensions...

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

            system_system_spacing = layouttools.make_spacing_vector(0, 0, 20, 0)
            lilypond_file.paper_block.system_system_spacing = system_system_spacing

            lilypond_file.header_block.composer = markuptools.Markup('Randall West')

            # TO DO... move "for Taiko and Orchestra" to subtitle
            lilypond_file.header_block.title = markuptools.Markup(self.title)

            return lilypond_file

        elif self.layout =="orchestra":
            #configure the score ... 
            spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
            override(self.score).vertical_axis_group.staff_staff_spacing = spacing_vector
            override(self.score).staff_grouper.staff_staff_spacing = spacing_vector
            override(self.score).staff_symbol.thickness = 0.5
            set_(self.score).mark_formatter = schemetools.Scheme('format-mark-box-numbers')

            lilypond_file = lilypondfiletools.make_basic_lilypond_file(self.score)

            # configure the lilypond file...
            lilypond_file.global_staff_size = 12

            context_block = lilypondfiletools.ContextBlock(
                #source_context_name="Staff \RemoveEmptyStaves",
                )
            override(context_block).vertical_axis_group.remove_first = True
            lilypond_file.layout_block.items.append(context_block)

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

            return lilypond_file

    def make_pdf(self, subfolder = None, part_names = None):
        """
        similar to abjad's builtin show()... but uses arrangement-specific file path/name instead of the abjad default,
        creates and returns pdf filename without showing it, and pdf file name does NOT increment
        """
        self.make_score(part_names=part_names)
        lilypond_file = self.make_lilypond_file()
        # print(format(lilypond_file))
        assert '__illustrate__' in dir(lilypond_file)
        result = topleveltools.persist(lilypond_file).as_pdf()
        pdf_file_path = result[0]
        abjad_formatting_time = result[1]
        lilypond_rendering_time = result[2]
        success = result[3]
        if success:
            # not sure why save_last_pdf_as doesn't work (UnicodeDecodeError)... so just using copyfile instead
            #systemtools.IOManager.save_last_pdf_as(project_pdf_file_path)
            project_pdf_file_path = self.pdf_path(subfolder)
            copyfile(pdf_file_path, project_pdf_file_path)

            return project_pdf_file_path
        if return_timing:
            return abjad_formatting_time, lilypond_rendering_time

    def show_pdf(self, part_names = None):
        """
        calls make_pdf and then shows the pdf: similar to abjad's builtin show() method... 
        but uses arrangement-specific file path/name instead of the abjad default 
        and pdf filename does NOT increment
        """
        print("")
        print("---------------------------------------------------------------------------")
        print("Creating PDF...")
        print("---------------------------------------------------------------------------")
        print("")

        pdf_file_path = self.make_pdf(part_names=part_names)
        systemtools.IOManager.open_file(pdf_file_path)

    def append_arrangement(self, arrangement, divider=False, fill_rests=True, fill_skips=False):
        # TO DO... divider doesn't work (how to get different kinds of bar lengths in general?)

        self.fill_empty_parts_with_rests()
        arrangement.fill_empty_parts_with_rests()

        for part_name in self.parts:
            # if simultaneous lines (staves... e.g. piano/hap) in the part, then extend each line/staff
            if self.parts[part_name].is_simultaneous:
                for i, part_line in enumerate(self.parts[part_name]):
                    part_line.extend(arrangement.parts[part_name][i])
                    if divider:
                        bar_line = indicatortools.BarLine("||")
                        attach(bar_line, part_line[-1])
            else:
                self.parts[part_name].extend(arrangement.parts[part_name])
                if divider:
                    bar_line = indicatortools.BarLine("||")
                    attach(bar_line, self.parts[part_name][-1])




