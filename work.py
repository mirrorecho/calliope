from abjad import *
from collections import OrderedDict
from shutil import copyfile

import copy

from calliope.settings import *
from calliope.tools import music_from_durations

# TO DO... 
# TODAY
# - easily view any cycle or cycles...
# - - - easily view a cross section of parts accross cycles
# - arrange relative pitches (DONE... need to test)
# - all cycles transformations (DONE... need to work with it more)
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
# - function for writing string harmonic
# LATER (AFTER FEB!)
# - think about structure of bubbles... how well is it working out? given lilypond's performance?



class Project():
    def __init__(self, name, title="", output_path=OUTPUT_PATH):
        self.name = name
        self.output_path = output_path
        self.project_path = output_path + "/" + name
        self.pdf_path = self.project_path + "/" + PDF_SUBFOLDER
        self.data_path = self.project_path + "/" + DATA_SUBFOLDER
        self.ly_path = self.project_path + "/" + LY_SUBFOLDER

# Parts inherit from Staff?
class Part(Staff):

    def __init__(self, name, instrument=None, clef=None, context_name='Staff'):
        super().__init__(name=name, context_name=context_name) # why doesn't context name work?

        # these attribbutes even needed?
        self.instrument = instrument 
        self.context_name = context_name # TO DO... understand what these contexts are doing
        self.name = name
        self.start_clef = clef

        # if time_signature is not None:
        #     # if len(self) > 0:
        #     #     attach(copy.deepcopy(time_signature), self[0])
        #     # else:
        #     attach(copy.deepcopy(time_signature), self)
        
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
    def __init__(self, name, instrument=None, clef=None, context_name='RhythmicStaff'):
        super().__init__(name, instrument=instrument, clef=clef, context_name=context_name)

    
    # def make_staff(self):
    #     # question... what about hi/low type of things... better to explicitly specify number of staff lines? 
    #     staff = scoretools.Staff([], context_name='RhythmicStaff')
    #     attach(self.instrument, staff)
    #     staff.extend(self)
    #     return staff

# TO DO.. I ASSUME THIS NO LONGER WORKS!
class PianoStaffPart(StaffGroup):
    def __init__(self, name, instrument=None, clef=None, context_name='StaffGroup', time_signature=None):
        super().__init__(name=name, context_name=context_name) # why doesn't context name work?
        self.is_simultaneous = True
        self.append(scoretools.Staff()) # top staff
        self.append(scoretools.Staff()) # bottom staff

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
        
        # TO DO ... able to override treble/bass clefs
        attach(Clef(name='bass'), self[1])


class Bubble(Score):
    """
    A bubble of musical material!
    """
    def __init__(self, 
            name="full-score", 
            project=None, 
            title="Full Score", 
            layout="standard", 
            measures_durations = [(4,4)]*4, # should we allow this to be None to be more flexible?
            rest_measures = None,
            odd_meters = False
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

        self.free = False # whether it starts free
        self.ends_free = False # whether it ends free

        self.time_signatures = [TimeSignature(d) for d in measures_durations]
        self.name = name
        self.measures_durations = measures_durations
        self.odd_meters = odd_meters

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

        # useful for building up little rhythmic phrases and then arranging them by passing a list of names
        # .... NOTE... right now this is a dictionary of strings, but maybe a dictionary of musical containers...
        #              or even some other abjad object instead of dictionary may be better suited

        self.material = {}
        self.material["pitch"] = {}
        self.material["rhythm"] = {}

    def attach(self, attachments, part_names, indices=[[0]], attachment_type=None, *args, **kwargs):
        # if the dynamics list includes types other than Dynamic, convert those to Dynamic (will often include strings of the dynamics to keep code clean)
        if attachment_type is not None:
            for p_i, p_a in enumerate(attachments):
                for i, a in enumerate(p_a):
                    if not isinstance(a, attachment_type):
                        attachments[p_i][i] = attachment_type(a)

        for i, part_name in enumerate(part_names):
            part_attachments = attachments[i % len(attachments)]
            part_indices = indices[i % len(indices)]
            part_material = self.parts[part_name].select_notes_and_chords()
            part_material_len = len(part_material)
            for j, n in enumerate(part_indices):
                if n < part_material_len:
                    attachment = part_attachments[j % len(part_attachments)]
                    attach(attachment, part_material[n])
                else:
                    print("Warning... attempted to add attachment at indice greater than length of material! Skipping attachment...")

    def attach_dynamics(self, dynamics, *args, **kwargs):
        self.attach(attachments=dynamics, attachment_type=indicatortools.Dynamic, *args, **kwargs)

    def attach_articulations(self, articulations, *args, **kwargs):
        self.attach(attachments=articulations, attachment_type=indicatortools.Articulation, *args, **kwargs)

    # note... only supports a single spanner per part at a time
    def attach_spanners(self, spanners, part_names, indices=((None,None)), *args, **kwargs):
        for i, part_name in enumerate(part_names):
            part_spanner = spanner[i % len(spanners)]
            part_indices = indices[i % len(indices)] # this will be the start and stop of the spanner
            part_material = self.parts[part_name].select_notes_and_chords()

            attach(part_spanner, part_material[part_indices[0]:part_indices[1]])
                   

    def arrange_music(self, 
                    part_names, 
                    rhythms=None, 
                    rhythm_material=None, 
                    pitches=None, 
                    pitch_material=None, 
                    respell=[None], 
                    respell_material=None, # respell material must be the name of a list
                    transpose=[0],
                    pitch_range=[None],
                    split_durations=[None],
                    pitch_offset=[0],
                    *args, **kwargs
                    ):
        #print("starting arrange...")
        for i, part_name in enumerate(part_names):

            # TO DO... could tidy up this logic...
            if rhythms is not None:
                if isinstance(rhythms, (list, tuple)):
                    # then this should be a list of actual rhythm stuff for each part

                    rhythm_stuff = rhythms[i % len(rhythms)]
                    
                    if isinstance(rhythm_stuff, (list, tuple)):
                        # then this is a list of rhythms for the part that need to be put together in a container
                        arrange_rhythm = Container()
                        for r in rhythm_stuff:
                            arrange_rhythm.extend(copy.deepcopy(r))
                    else:
                        # otherwise it's a single rhythm (as a string or container)
                        arrange_rhythm = rhythm_stuff
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

                # then the pitch material should either be a list or matrix of rhythm names
                pitch_stuff = pitch_material[i % len(pitch_material)]
                if isinstance(pitch_stuff, str):
                    # then this is the name of pitch material 
                    arrange_pitches = self.material["pitch"][pitch_stuff]
                elif isinstance(pitch_stuff, (list, tuple)):
                    # then this is a list of pitch material names ( in a row )
                    arrange_pitches=copy.deepcopy(self.material["pitch"][pitch_stuff[0]])
                    for extend_name in pitch_stuff[1:]:
                        arrange_pitches.extend(self.material["pitch"][extend_name])
                else:
                    arrange_pitch = 0
                    print("Warning... unexpected type of pitch material passed")

            else:
                arrange_pitches = None

            if respell_material is not None:
                respell = self.material[respell_material]   
            arrange_respell = respell[i % len(respell)]

            arrange_transpose = transpose[i % len(transpose)]
            arrange_pitch_range = pitch_range[i % len(pitch_range)]
            arrange_split_durations = split_durations[i % len(split_durations)]
            arrange_pitch_offset = pitch_offset[i % len(pitch_offset)]

            music = music_from_durations(
                durations=arrange_rhythm, 
                pitches=arrange_pitches, 
                transpose=arrange_transpose, 
                respell=arrange_respell, 
                split_durations=arrange_split_durations,
                pitch_offset=arrange_pitch_offset
                )
            
            if arrange_pitch_range is not None:
                # QUESTION... does this work for chords or to they need to be handled separately?
                for i, note in enumerate(iterate(music).by_class(Note)):
                    note.written_pitch = pitchtools.transpose_pitch_expr_into_pitch_range([note.written_pitch.pitch_number], arrange_pitch_range)[0]

            # TO DO... could pass along split durations here...
            
            if self.free:
                # free music has a single variable length measure
                self.parts[part_name][0].append(music)
            elif self.odd_meters:
                # changing odd meters requires this stupid hack:
                funny_dumbass_measure = Measure((1,8))
                funny_dumbass_measure.extend(music)
                odd_measures = mutate(funny_dumbass_measure).split(self.measures_durations)
                self.parts[part_name].extend(odd_measures)
            else:
                self.parts[part_name].extend(music)

            #part = self.parts[part_name]
            #part[0].extend(music)
            #mutate(part[0]).split(self.measures_durations)
            #scoretools.append_spacer_skips_to_underfull_measures_in_expr(part)
            #mutate(part[0]).split(self.measures_durations)
            #part.
            #print("finished arrange...")

    def fill_empty_parts_with_skips(self):
        for part_name, part in self.parts.items():
            if part.is_simultaneous:
                print("filling empty rests on piano parts not supported...")
                # for part_line in part:
                #     if len(part.select_leaves()) == 0:
                #         part_line.extend(scoretools.make_spacer_skip_measures(self.measures_durations))
            elif len(part.select_leaves()) == 0:
                #if self.odd_meters:
                # for d in self.measures_durations:
                #     part.append(scoretools.Skip(d))
                # else:
                part.extend(scoretools.make_spacer_skip_measures(self.measures_durations))
                # c2 = Container()
                # c2.extend(c.select_leaves())
                # skips_string = format(c2)
                # #print(skips_string)
                # if self.odd_meters:
                #     part.extend("r1")

    def fill_empty_parts_with_rests(self):
        for part_name in self.parts:
            part = self.parts[part_name]
            if part.is_simultaneous:
                for part_line in part:
                    if len(part_line) == 0:
                        part_line.extend(copy.deepcopy(self.rest_measures))
            elif len(part.select_leaves()) == 0:
                for d in self.measures_durations:
                    part.extend(copy.deepcopy(self.rest_measures))

    def pdf_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.pdf_path + "/" + subfolder + self.project.name + "-" + self.name + ".pdf"

    def ly_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.ly_path + "/" + subfolder + self.project.name + "-" + self.name + ".ly"

    def add_part(self, name, instrument=None, clef=None):
        self.parts[name] = Part(name=name, instrument=instrument, clef=clef)
        #self.parts[name].append(self.rest_measures)

        if len(self.time_signatures) > 0:
            attach(copy.deepcopy(self.time_signatures[0]), self.parts[name])

        # for m in self.measures_durations:
        #     self.parts[name].append(Measure(m))

        # if score_append:
        #self.append(self.parts[name])

    def add_perc_part(self, name, instrument=None):
        self.parts[name] = PercussionPart(name=name, instrument=instrument)
        # for m in self.measures_durations:
        #     self.parts[name].append(Measure(m))
        # self.parts[name].append(self.rest_measures)
        if len(self.time_signatures) > 0:
            attach(copy.deepcopy(self.time_signatures[0]), self.parts[name])

        #self.append(self.parts[name])

    # doesn't work anymore....
    # def add_piano_staff_part(self, name, instrument=None):
    #     # not sure if this works for piano parts...
    #     self.parts[name] = PianoStaffPart(name=name, instrument=instrument, time_signature=self.time_signature)
    #     self.append(self.parts[name])

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
            lilypond_file.global_staff_size = 13

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

            with open(self.ly_path(), "w") as ly_file:
                ly_file.write(format(lilypond_file))

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
            measures_durations = self.measures_durations)

        for p in part_names:
            # is it OK that we're not making a copy of this...??
            bubble.parts[p] = self.parts[p]
            bubble.append(bubble.parts[p])

        return bubble


    def make_score(self):
        for part_name, part in self.parts.items():

            attach(part.instrument, part)

            numeric_time_command = indicatortools.LilyPondCommand("numericTimeSignature","before")
            # OK to assume that the part contains stuff?
            attach(numeric_time_command, part[0])

            self.append(part)

        self.prepare_score()


    def make_pdf(self, subfolder = None, part_names = None, fill_skips=False):
        """
        similar to abjad's builtin show()... but uses bubble-specific file path/name instead of the abjad default,
        creates and returns pdf filename without showing it, and pdf file name does NOT increment
        """
        self.make_score()

        if fill_skips:
            scoretools.append_spacer_skips_to_underfull_measures_in_expr(self)

        if part_names is not None:
            bubble = self.make_fragment_bubble(part_names)
        else:
            bubble = self

        lilypond_file = bubble.make_lilypond_file()

        print("RUNNING LILYPOND NOW...")

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

    def append_bubble(self, bubble, divider=False, fill_rests=False, fill_skips=True, fill_self=True):
        # TO DO... divider doesn't work (how to get different kinds of bar lengths in general?)

        # needed anymore...??
        if bubble.free:
            bubble.align_parts()
        if fill_rests:
            if fill_self:
                self.fill_empty_parts_with_rests()
            bubble.fill_empty_parts_with_rests()
        if fill_skips:
            if fill_self:
                self.fill_empty_parts_with_skips()
            bubble.fill_empty_parts_with_skips()

        # TO DO... combine this with the loop below... should be no reason to loop through all the parts twice
        if bubble.free:
            bubble.show_x_time = not self.ends_free
            bubble.x_time_signatures()

        for part_name in self.parts:
            if len(bubble.time_signatures) > 0 and len(self.time_signatures) > 0 and len(bubble.parts[part_name]) > 0 and bubble.time_signatures[0] != self.time_signatures[-1]:
                # time signatures attached to staff are not copied over with extend... 
                # so attach bubble's time signature to the music inside the staff
                # first so that it is copied 
                
                # if odd meters, then the time signatures are already in the measures...

                if bubble.odd_meters and not bubble.free:
                    attach(copy.deepcopy(bubble.time_signatures[0]), bubble.parts[part_name])

            # if simultaneous lines (staves... e.g. piano/hap) in the part, then extend each line/staff
            if self.parts[part_name].is_simultaneous:
                print("simultaneous bubble appends not supported....")
                # for i, part_line in enumerate(self.parts[part_name]):
                #     if divider and len(part_line) > 0:
                #         bar_line = indicatortools.BarLine("||")
                #         attach(bar_line, part_line[-1])
                #     part_line.extend(bubble.parts[part_name][i])

            else:
                if divider and len(self.parts[part_name]) > 0:
                    bar_line = indicatortools.BarLine("||")
                    # TO DO... THIS IS TERRIBLE!
                    # So haky!!!!
                    try:
                        if isinstance(self.parts[part_name][-1], Measure) and len(self.parts[part_name][-1])>0:
                            attach(bar_line, self.parts[part_name][-1][-1])
                        else:
                            attach(bar_line, self.parts[part_name][-1])
                    except:
                        pass
                self.parts[part_name].extend(bubble.parts[part_name])

        self.measures_durations += bubble.measures_durations
        self.time_signatures += bubble.time_signatures
        self.ends_free = bubble.free



