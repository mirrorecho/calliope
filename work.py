from abjad import *
from collections import OrderedDict
from shutil import copyfile

import copy

from calliope.settings import *
from calliope.tools import music_from_durations

# TO DO... 
# TODAY
# - arrange relative pitches (DONE... need to test)
# - all cycles transformations
# - easily load cloud pitches into pitch material
# SOON
# - speed it up!!!! (minimize # of parts?) ...what's the main bottleneck? inheriting from Score?
# - some kind of warning/error msg if material doesn't exist in dictionary when arranging
# - resurrect previous cycle transforms?
# - - - cloud pitches?
# - - - copy music?
# - - - copy pitch?
# - - - make lines (as raw material... before arranging to parts)?
# - what about cells... are these even useful anymore?
# - staff groups
# - allow overlays (parts on parts and material on material)
# - material dictionary for lines?
# - use assertions...
# - question is it OK to treat material like strings (add it with other strings?)... or should it be more abstract?
# - use measures durations here....
# - option to hide empty parts/staves
# - fill parts with rests/skips
# - arrange at certain duration
# - specify paper/book/misc lilypond output settings
# - fragment bubble could be extended for parts, other copies, etc.


class Project():
    def __init__(self, name, title="", output_path=OUTPUT_PATH):
        self.name = name
        self.output_path = output_path
        self.project_path = output_path + "/" + name
        self.pdf_path = self.project_path + "/" + PDF_SUBFOLDER
        self.data_path = self.project_path + "/" + DATA_SUBFOLDER

# Parts inherit from Staff?
class Part(Staff):

    def __init__(self, name, instrument=None, clef=None, context_name='Staff', time_signature=None):
        super().__init__(name=name, context_name=context_name) # why doesn't context name work?

        # these attribbutes even needed?
        self.instrument = instrument 
        self.context_name = context_name # TO DO... understand what these contexts are doing
        self.name = name
        self.start_clef = clef

        if time_signature is not None:
            # if len(self) > 0:
            #     attach(copy.deepcopy(time_signature), self[0])
            # else:
            attach(copy.deepcopy(time_signature), self)
        
        attach(self.instrument, self)
        
        if clef is not None:
            attach(Clef(name=clef), self)

# TO USE FOR SONGS TEMPORARILY
# class Part(scoretools.Context):

#     def __init__(self, name, instrument=None, clef=None, context_name='Staff'):
#         self.instrument = instrument
#         self.start_clef = clef
#         super().__init__()
#         self.context_name = name

#     def make_staff(self):
#         staff = scoretools.Staff([])
#         attach(self.instrument, staff)
#         if self.start_clef is not None:
#             attach(Clef(name=self.start_clef), staff)
#         staff.extend(self)
#         return staff


class PercussionPart(Part):
    def __init__(self, name, instrument=None, clef=None, context_name='RhythmicStaff', time_signature=None):
        super().__init__(name, instrument=instrument, clef=clef, context_name=context_name, time_signature=time_signature)

    
    # def make_staff(self):
    #     # question... what about hi/low type of things... better to explicitly specify number of staff lines? 
    #     staff = scoretools.Staff([], context_name='RhythmicStaff')
    #     attach(self.instrument, staff)
    #     staff.extend(self)
    #     return staff

class PianoStaffPart(Part):

    def __init__(self, name, instrument=None, time_signature=None):
        super().__init__(name=name, instrument=instrument, time_signature=time_signature)
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

class Bubble(Score):
    """
    A bubble of musical material!
    """
    def __init__(self, 
            name="full-score", 
            project=None, 
            title="Full Score", 
            layout="standard", 
            time_signature=TimeSignature( (4,4) ),
            measures_durations = [(4,4)]*4, # should we allow this to be None to be more flexible?
            rest_measures = None,
            ):
        
        super().__init__()

        self.parts = OrderedDict() # assume this is necessary... unless there's some way to get score staves by name
        
        self.output_path = OUTPUT_PATH
        self.layout = layout
        if project is not None:
            self.project = project
        else:
            self.project = Project("rwestmusic")
        self.title = title

        self.time_signature = time_signature
        self.last_time_signature = time_signature # the last time signature... useful for appending
            # new bubbles and deciding if a new time signature indication is needed or not
        self.name = name
        self.measures_durations = measures_durations

        # right now this is being used to deterimne the length (i.e. to fil with rests)
        # ... some better way to handle?
        if rest_measures is not None:
            # useful for specifying rest measures for non assignable measure durations (e.g. something like 9/8)
            self.rest_measures = rest_measures
        else:
            # if any measure duration is not assignable as a multi measure rest (e.g. something like 9/8),
            # then fall fall back to standard rests instead of multi measure rests
            if any([not Duration(d).is_assignable for d in measures_durations]):
                self.rest_measures = scoretools.make_rests(measures_durations)
            else:
                self.rest_measures = scoretools.make_multimeasure_rests(measures_durations)
        self.skip_measures = scoretools.make_spacer_skip_measures(measures_durations)

        # useful for building up little rhythmic phrases and then arranging them by passing a list of names
        # .... NOTE... right now this is a dictionary of strings, but maybe a dictionary of musical containers...
        #              or even some other abjad object instead of dictionary may be better suited

        self.material = {}
        self.material["pitch"] = {}
        self.material["rhythm"] = {}

        # # similarly, for building up 
        # self.pitch_material = {}

        # (
        # part_names=["part1", "part2"],
        
        # rhythms = ["r4^part1 c2.","r4^part2 c4 c4 c4"]
        # # OR
        # rhythm_material=[
        #     ["rhythm1_A","rhythm1_B"],
        #     ["rhythm2_A","rhythm2_B"],
        #     ]
        # # OR
        # rhythm_material=["rhythm1","rhythm2"]
        # # OR
        # rhythm_material="rhythm_matrix"

        # # if pitches passed, it must be a list of pitch row lists 
        # pitches = [["A4", "C#4"]]
        # # OR
        # pitch_material = ["pitch_row_A", "pitch_row_B"]
        # # OR
        # pitch_material = "pitches_matrix"
        # )

    def arrange_music(self, 
                    part_names, 
                    rhythms=None, 
                    rhythm_material=None, 
                    pitches=None, 
                    pitch_material=None, 
                    respell=[None], 
                    transpose=[0],
                    pitch_range=[None],
                    split_durations=[None],
                    *args, **kwargs
                    ):
        for i, part_name in enumerate(part_names):

            # TO DO... could tidy up this logic...
            if rhythms is not None:
                if isinstance(rhythms, (list, tuple)):
                    # then this should be a list of the actual rhythms
                    arrange_rhythm = rhythms[i % len(rhythms)]
                else:
                    arrange_rhythm = "R1 "
                    print("----------------------------------------------")
                    print("WARNING... unexpected type of rhythms passed when attempting to arrange to " + ", ".join(part_names))
                    print("Exected list, got " + type(rhythms).__name__)
                    print("Replacing with rest...")
                    print("----------------------------------------------")
            elif isinstance(rhythm_material, str):
                # then the rhythm material should be the name of a rhythm list... get the right rhythm
                rhythm_list = self.material["rhythm"][rhythm_material]
                arrange_rhythm = rhythm_list[i % len(rhythm_list)]
            elif isinstance(rhythm_material, (list, tuple)):
                # then the rhythm material should either be a list or matrix of rhythm names
                rhythm_stuff = rhythm_material[i % len(rhythm_material)]
                if isinstance(rhythm_stuff, str):
                    # then this the name of rhythm material 
                    arrange_rhythm = self.material["rhythm"][rhythm_stuff]
                elif isinstance(rhythm_stuff, (list, tuple)):
                    arrange_rhythm = " ".join([self.material["rhythm"][r] for r in rhythm_stuff])
                    # then this is a list of rhythm material names ( in a row )
                else:
                    arrange_rhythm = "R1 "
                    print("Warning... unexpected type of rhythm material passed")
            else:
                arrange_rhythm = "R1 "
                print("Warning... unexpected type of rhythm material passed")

            if pitches is not None:
                # then this should be a matrix of the actual pitches
                arrange_pitches = pitches[i % len(pitches)]
            elif isinstance(pitch_material, str):
                # then the pitch material should be the name of a pitch matrix... get the right row
                pitch_matrix = self.material["pitch"][pitch_material]
                arrange_pitches = pitch_matrix[i % len(pitch_matrix)]
            elif isinstance(pitch_material, (list, tuple)):
                # then the pitch material should be the names of a pitch rows...
                arrange_pitches = self.material["pitch"][pitch_material[i % len(pitch_material)]]
            else:
                arrange_pitches = None

            arrange_respell = respell[i % len(respell)]
            arrange_transpose = transpose[i % len(transpose)]
            arrange_pitch_range = pitch_range[i % len(pitch_range)]
            arrange_split_durations = split_durations[i % len(split_durations)]

            music = music_from_durations(durations=arrange_rhythm, pitches=arrange_pitches, transpose=arrange_transpose, respell=arrange_respell, split_durations=arrange_split_durations)
            
            if arrange_pitch_range is not None:
                # QUESTION... does this work for chords or to they need to be handled separately?
                for i, note in enumerate(iterate(music).by_class(Note)):
                    note.written_pitch = pitchtools.transpose_pitch_expr_into_pitch_range([note.written_pitch.pitch_number], arrange_pitch_range)[0]

            # TO DO... could pass along split durations here...
            self.parts[part_name].extend(music)


    def fill_empty_parts_with_skips(self):
        for part_name in self.parts:
            part = self.parts[part_name]
            if part.is_simultaneous:
                for part_line in part:
                    if len(part_line) == 0:
                        part_line.extend(copy.deepcopy(self.skip_measures))
            elif len(part) == 0:
                part.extend(copy.deepcopy(self.skip_measures))

    def fill_empty_parts_with_rests(self):
        for part_name in self.parts:
            part = self.parts[part_name]
            if part.is_simultaneous:
                for part_line in part:
                    if len(part_line) == 0:
                        part_line.extend(copy.deepcopy(self.rest_measures))
            elif len(part) == 0:
                part.extend(copy.deepcopy(self.rest_measures))

    def pdf_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.pdf_path + "/" + subfolder + self.project.name + "-" + self.name + ".pdf"

    def add_part(self, name, instrument=None, clef=None):
        self.parts[name] = Part(name=name, instrument=instrument, clef=clef, time_signature=self.time_signature)
        self.append(self.parts[name])

    def add_perc_part(self, name, instrument=None):
        self.parts[name] = PercussionPart(name=name, instrument=instrument, time_signature=self.time_signature)
        self.append(self.parts[name])

    def add_piano_staff_part(self, name, instrument=None):
        # not sure if this works for piano parts...
        self.parts[name] = PianoStaffPart(name=name, instrument=instrument, time_signature=self.time_signature)
        self.append(self.parts[name])

    def prepare_score(self):
        """ this is a hook that derived classes can override to modify the score before 
        going to print """
        pass


    def make_lilypond_file(self):
        """
        Makes Lilypond File
        """
        if self.layout == "standard":
            #configure the score ... 
            # spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
            # override(self.score).vertical_axis_group.staff_staff_spacing = spacing_vector
            # override(self.score).staff_grouper.staff_staff_spacing = spacing_vector
            set_(self).mark_formatter = schemetools.Scheme('format-mark-box-numbers')
            lilypond_file = lilypondfiletools.make_basic_lilypond_file(self)

            # configure the lilypond file...
            lilypond_file.global_staff_size = 16

            staff_context_block = lilypondfiletools.ContextBlock(
                source_context_name="Staff \\RemoveEmptyStaves",
                )
            override(staff_context_block).vertical_axis_group.remove_first = True
            lilypond_file.layout_block.items.append(staff_context_block)

            rhythmic_staff_context_block = lilypondfiletools.ContextBlock(
                source_context_name="RhythmicStaff \\RemoveEmptyStaves",
                )
            override(rhythmic_staff_context_block).vertical_axis_group.remove_first = True
            lilypond_file.layout_block.items.append(rhythmic_staff_context_block)

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
            override(self).vertical_axis_group.staff_staff_spacing = spacing_vector
            override(self).staff_grouper.staff_staff_spacing = spacing_vector
            override(self).staff_symbol.thickness = 0.5
            set_(self).mark_formatter = schemetools.Scheme('format-mark-box-numbers')

            lilypond_file = lilypondfiletools.make_basic_lilypond_file(self)

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


    def make_fragment_bubble(self, part_names):
        """
        creates a new bubble instance with a subset of this bubble's parts (ONLY)
        """
        # not the most elegent solution... but this should work...
        bubble = Bubble(
            name=self.name + "-fragment", 
            project=self.project, 
            title=self.title, 
            layout=self.layout, 
            time_signature=self.time_signature,
            measures_durations = self.measures_durations)

        for p in part_names:
            # is it OK that we're not making a copy of this...??
            bubble.parts[p] = self.parts[p]
            bubble.append(bubble.parts[p])

        return bubble


    def make_pdf(self, subfolder = None, part_names = None):
        """
        similar to abjad's builtin show()... but uses bubble-specific file path/name instead of the abjad default,
        creates and returns pdf filename without showing it, and pdf file name does NOT increment
        """
        self.prepare_score()

        if part_names is not None:
            bubble = self.make_fragment_bubble(part_names)
        else:
            bubble = self

        lilypond_file = bubble.make_lilypond_file()

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
            project_pdf_file_path = bubble.pdf_path(subfolder)
            copyfile(pdf_file_path, project_pdf_file_path)

            return project_pdf_file_path
        if return_timing:
            return abjad_formatting_time, lilypond_rendering_time

    def show_pdf(self, part_names = None):
        """
        calls make_pdf and then shows the pdf: similar to abjad's builtin show() method... 
        but uses bubble-specific file path/name instead of the abjad default 
        and pdf filename does NOT increment
        """
        print("")
        print("---------------------------------------------------------------------------")
        print("Creating PDF...")
        print("---------------------------------------------------------------------------")
        print("")

        pdf_file_path = self.make_pdf(part_names=part_names)
        systemtools.IOManager.open_file(pdf_file_path)

    def append_bubble(self, bubble, divider=False, fill_rests=True, fill_skips=False):
        # TO DO... divider doesn't work (how to get different kinds of bar lengths in general?)

        self.fill_empty_parts_with_rests()
        bubble.fill_empty_parts_with_rests()

        for part_name in self.parts:
            if bubble.time_signature != self.last_time_signature:
                # time signatures attached to staff are not copied over with extend... 
                # so attach bubble's time signature to the music inside the staff
                # first so that it is copied 
                attach(bubble.time_signature, bubble.parts[part_name][0])

            # if simultaneous lines (staves... e.g. piano/hap) in the part, then extend each line/staff
            if self.parts[part_name].is_simultaneous:
                for i, part_line in enumerate(self.parts[part_name]):
                    part_line.extend(bubble.parts[part_name][i])
                    if divider:
                        bar_line = indicatortools.BarLine("||")
                        attach(bar_line, part_line[-1])
            else:
                self.parts[part_name].extend(bubble.parts[part_name])
                if divider:
                    bar_line = indicatortools.BarLine("||")
                    attach(bar_line, self.parts[part_name][-1])

        self.last_time_signature = bubble.time_signature



