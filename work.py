from abjad import *
from collections import OrderedDict
from shutil import copyfile

import copy

from calliope.settings import *
from calliope.tools import *

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

class PartGroup(scoretools.StaffGroup):
    def __init__(self, name, part_names):
        super().__init__(name=name)
        self.part_names = part_names
        self.title = None

class Part(Staff):

    def __init__(self, name, instrument=None, clef=None, context_name='Staff', master_part_name=None, resize=0):
        super().__init__(name=name, context_name=context_name) # why doesn't context name work?

        self.master_part_name = master_part_name
        if master_part_name is not None:
            self.is_sub_part = True
        else:
            self.is_sub_part = False

        self.sub_show_instrument_instruction = False

        self.is_arranged = False # used to indicate whether music has been arranged to this part for a particular bubble

        #self.prepared = False

        # TO DO EVENTUALLY... BAD BAD ... super hacky work-around for dealing with X time signature attachments and sub parts....
        self.first_item = None

        self.sub_part_names =[]
        self.is_compound = False

        self.subs_replace = False # if true, then the music for the last sub part will be placed on this staff
        self.resize = resize

        # these attribbutes even needed?
        self.instrument = instrument 
        self.sub_instrument_name = None
        self.sub_short_instrument_name = None
        self.context_name = context_name # TO DO... understand what these contexts are doing
        self.name = name
        self.start_clef = clef
        self.staff_group_name = None

    def append_part(self, new_part, divider=False):
        if divider and len(self) > 0:
            bar_line = indicatortools.BarLine("||")
            # TO DO... THIS IS TERRIBLE!
            # So haky!!!!
            try:
                if isinstance(self[-1], Measure) and len(self[-1])>0:
                    attach(bar_line, self[-1][-1])
                else:
                    attach(bar_line, self[-1])
            except:
                pass
        
            # if simultaneous lines (staves... e.g. piano/hap) in the part, then extend each line/staff
            # if self.parts[part_name].is_simultaneous:
            #     print("simultaneous bubble appends not supported....")
            #     # for i, part_line in enumerate(self.parts[part_name]):
            #     #     if divider and len(part_line) > 0:
            #     #         bar_line = indicatortools.BarLine("||")
            #     #         attach(bar_line, part_line[-1])
            #     #     part_line.extend(bubble.parts[part_name][i])

            #  else:

        # TO DO... document this!!!
        if self.is_compound:
            if new_part.is_compound:
                self[-1][-1].extend(new_part[-1][-1])
            else:
                self[-1][-1].extend(new_part)
        else:
            self.extend(new_part)

        self.is_compound = new_part.is_compound

        # if time_signature is not None:
        #     # if len(self) > 0:
        #     #     attach(copy.deepcopy(time_signature), self[0])
        #     # else:
        #     attach(copy.deepcopy(time_signature), self)
    

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
        
        self.parts_prepared = False # indicates whether all subparts have been made, rests added, instruments added, etc.
        self.compound_part_names = [] # just an easy way to keep track of this so we don't always have to loop through all the parts

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
        self.staff_groups = OrderedDict()

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

    def copy_material(self, material_type, material, copy_to):
        self.material[material_type][copy_to] = copy.deepcopy(self.material[material_type][material])

    def transpose_pitch_material(self, material, transpose):
        self.material["pitch"][material] = transpose_pitches(self.material["pitch"][material], transpose)

    def attach(self, attachments, part_names, indices=[[0]], notes_only=[True], attachment_type=None, *args, **kwargs):
        # if the dynamics list includes types other than Dynamic, convert those to Dynamic (will often include strings of the dynamics to keep code clean)
        if attachment_type is not None:
            for p_i, p_a in enumerate(attachments):
                for i, a in enumerate(p_a):
                    if not isinstance(a, attachment_type):
                        attachments[p_i][i] = attachment_type(a)

        for i, part_name in enumerate(part_names):
            part_attachments = attachments[i % len(attachments)]
            part_indices = indices[i % len(indices)]
            part_notes_only = notes_only[i % len(notes_only)]
            if part_notes_only:
                part_material = self.parts[part_name].select_notes_and_chords()
            else:
                part_material = self.parts[part_name].select_leaves()
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

    def attach_markup(self, markup_texts, *args, **kwargs):
        markups = [[markuptools.Markup(m, direction=Up) for m in m_texts] for m_texts in markup_texts]
        self.attach(attachments=markups, *args, **kwargs)

    # note... only supports a single spanner per part at a time
    def attach_spanners(self, spanners, part_names, indices=((None,None)), *args, **kwargs):
        for i, part_name in enumerate(part_names):
            part_spanner = spanner[i % len(spanners)]
            part_indices = indices[i % len(indices)] # this will be the start and stop of the spanner
            part_material = self.parts[part_name].select_notes_and_chords()

            attach(part_spanner, part_material[part_indices[0]:part_indices[1]])
                   
    def arrange_music(self, 
                    part_names, 
                    sub_part_names = None, # should be a list the same length as part_names 
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
                    pitch_rows=[None],
                    pitch_columns=[None],
                    replace = [False], # NOT SUPPORTED YET
                    skip_arranged = [True],
                    harmonics_make = [False],
                    harmonics_args = [{}],
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

            arrange_pitch_rows = pitch_rows[i % len(pitch_rows)]
            if arrange_pitch_rows is not None:
                p_i = arrange_pitch_rows
            else:
                p_i = i

            if pitches is not None:
                # then this should be a matrix of the actual pitches, so just get our row of pitches:
                arrange_pitches = pitches[p_i % len(pitches)]
            elif isinstance(pitch_material, str):
                # then the pitch material should be the name of a pitch matrix... get the right row from the material
                pitch_matrix = self.material["pitch"][pitch_material]
                arrange_pitches = pitch_matrix[p_i % len(pitch_matrix)]
            elif isinstance(pitch_material, (list, tuple)):
                # then the pitch material should be the names of a pitch rows...
                # get the material name or list of names for our row:
                pitch_stuff = pitch_material[p_i % len(pitch_material)]
                
                if isinstance(pitch_stuff, str):
                    # then this is the name of pitch material 
                    arrange_pitches = self.material["pitch"][pitch_stuff]
                elif isinstance(pitch_stuff, (list, tuple)):
                    # then this is a list of pitch material names ( to be extended into a single row )
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
            arrange_replace = replace[i % len(replace)]
            arrange_skip_arranged = skip_arranged[i % len(skip_arranged)]
            arrange_harmonics_make = harmonics_make[i % len(harmonics_make)]
            arrange_harmonics_args = harmonics_args[i % len(harmonics_args)]
            arrange_pitch_columns = pitch_columns[i % len(pitch_columns)]

            music = music_from_durations(
                durations=arrange_rhythm, 
                pitches=arrange_pitches, 
                transpose=arrange_transpose, 
                respell=arrange_respell, 
                split_durations=arrange_split_durations,
                pitch_offset=arrange_pitch_offset,
                pitch_columns = arrange_pitch_columns
                )
            
            if arrange_pitch_range is not None:
                # QUESTION... does this work for chords or to they need to be handled separately?
                for i, note in enumerate(iterate(music).by_class(Note)):
                    note.written_pitch = pitchtools.transpose_pitch_expr_into_pitch_range([note.written_pitch.pitch_number], arrange_pitch_range)[0]

            # TO DO... could pass along split durations here...

            if arrange_harmonics_make:
                make_harmonics(music, **arrange_harmonics_args)
            
            if (not arrange_skip_arranged) or (not self.parts[part_name].is_arranged):
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

            self.parts[part_name].is_arranged = True

            #part = self.parts[part_name]
            #part[0].extend(music)
            #mutate(part[0]).split(self.measures_durations)
            #scoretools.append_spacer_skips_to_underfull_measures_in_expr(part)
            #mutate(part[0]).split(self.measures_durations)
            #part.
            #print("finished arrange...")

    # def make_harmonics(self, part_names, *args, **kwargs):
    #     for part_name in part_names:
    #         make_harmonics(self.parts[part_name], *args, **kwargs)

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

    # TO DO... maybe this function should go on the part, not on the bubble
    def change_instrument(self, part_name, instrument_name, short_instrument_name, show_instruction=True, instruction_text=None, attach_before=None):
        instrument_command = indicatortools.LilyPondCommand("set Staff.instrumentName = \\markup { " + instrument_name + " }", "before")
        short_instrument_command = indicatortools.LilyPondCommand("set Staff.shortInstrumentName = \\markup { " + short_instrument_name + " }", "before")
        if attach_before is None:
            if len(self.parts[part_name]) > 0:
                attach_before = self.parts[part_name][0]
            else:
                print("Error: can't attach " + instrument_name + " instrument change to part " + part_name + " because this part is empty.")
                return
        attach(instrument_command, attach_before)
        attach(short_instrument_command, attach_before)
        if show_instruction:
            if instruction_text is None:
                instruction_text = instrument_name
            instruction_markup = markuptools.Markup('\italic { "' + instruction_text + '" }', direction=Up)
            attach(instruction_markup, attach_before)

    # NOTE... title not supported yet...
    def add_staff_group(self, name, part_names, title=None):
        # TO DO EVENTUALLY... deal with part groups as real material....
        self.staff_groups[name] = PartGroup(name=name, part_names=part_names)
        self.staff_groups[name].title = title

    def add_part(self, name, instrument=None, clef=None):
        self.parts[name] = Part(name=name, instrument=instrument, clef=clef)
        #self.parts[name].append(self.rest_measures)

        if len(self.time_signatures) > 0:
            attach(copy.deepcopy(self.time_signatures[0]), self.parts[name])

        # for m in self.measures_durations:
        #     self.parts[name].append(Measure(m))

        # if score_append:
        #self.append(self.parts[name])

    def add_sub_part(self, part_name, master_part_name, instrument_name=None, short_instrument_name=None, instrument_type=None, show_instrument_instruction=False, clef=None, replace_master_part = True):
        # # this throws duplicate indicator error for some STUPID reason...
        # master_instrument = self.parts[master_part_name].instrument
        # if instrument_type is None:
        #     instrument_type = type(master_instrument)
        # if instrument_name is None:
        #     instrument_name = master_instrument.instrument_name
        # if short_instrument_name is None:
        #     short_instrument_name = master_instrument.short_instrument_name
        # instrument = instrument_type(instrument_name=instrument_name, short_instrument_name=short_instrument_name)
        if instrument_type is None:
            instrument = copy.deepcopy(self.parts[master_part_name].instrument)
        else:
            instrument = instrument_type()
        self.parts[part_name] = Part(name=part_name, instrument=instrument, clef=clef, master_part_name=master_part_name)
        self.parts[part_name].sub_instrument_name = instrument_name
        self.parts[part_name].sub_short_instrument_name = short_instrument_name
        self.parts[part_name].sub_show_instrument_instruction = show_instrument_instruction
        if self.free:
            free_measure = Measure(self.measures_durations[0])
            free_measure.automatically_adjust_time_signature = True
            self.parts[part_name].append(free_measure)
            
        self.parts[master_part_name].sub_part_names.append(part_name)
        if master_part_name not in self.compound_part_names:
            self.compound_part_names.append(master_part_name)
        # note... this applies to the master part for ALL concurrent sub parts
        self.parts[master_part_name].subs_replace = replace_master_part

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
            if p in self.parts:
                bubble.parts[p] = self.parts[p]
                bubble.append(bubble.parts[p])

        return bubble


    def make_score(self):

        self.prepare_parts()

        # this is a little hacky...
        for staff_group_name, staff_group in self.staff_groups.items():
            self.append(staff_group)
            for part_name in staff_group.part_names:
                if part_name in self.parts:
                    self.parts[part_name].staff_group_name = staff_group_name
                else:
                    print("Warning... " + part_name + " included in staff group, but does not exist as a part.")

        for part_name, part in self.parts.items():

            if len(part) > 0:
                attach(part.instrument, part)
                # print("Error attaching instrument to part: " + part_name)
                numeric_time_command = indicatortools.LilyPondCommand("numericTimeSignature","before")
                # OK to assume that the part contains stuff?
                attach(numeric_time_command, part[0])

            if part.start_clef is not None:
                attach(Clef(name=part.start_clef), part)

            if not part.is_sub_part:
                if part.staff_group_name is not None:
                    self.staff_groups[part.staff_group_name].append(part)
                else:
                    self.append(part)

        self.prepare_score()


    def prepare_parts(self, existing_compound_part_names=[]):
        # TO DO... allow filling with skips OR rests
        if not self.parts_prepared:

            # TO DO EVENTUALLY... not great looping through all the parts here again... to add these
            # accidental styles, but there was an issue appending this only at the beginning of the
            # big bubble if the first bubble attached to it was free
            for part_name, part in self.parts.items():
                if not self.free and len(part)>0:
                    accidental_command = indicatortools.LilyPondCommand("context Staff {#(set-accidental-style 'modern)}", "before")
                    attach(accidental_command, part[0])

            for compound_part_name in self.compound_part_names:

                if compound_part_name not in existing_compound_part_names:
                    # this is so appends work out... if compound part already set up, then we shouldn't do anything here...

                    old_part = self.parts[compound_part_name]
                    self.parts[compound_part_name] = Part(compound_part_name) # TO DO??... append instrument, clef, etc.
                    self.parts[compound_part_name].is_compound = True
                    
                    compound_countainer = Container()
                    compound_countainer.is_simultaneous = True

                    bottom_part = old_part
                    
                    for i, sub_part_name in enumerate(old_part.sub_part_names):
                        sub_part = self.parts[sub_part_name]
                        if sub_part.sub_instrument_name is not None and sub_part.sub_short_instrument_name is not None:
                            self.change_instrument(part_name=sub_part_name, 
                                instrument_name=sub_part.sub_instrument_name, 
                                short_instrument_name=sub_part.sub_short_instrument_name,
                                show_instruction=sub_part.sub_show_instrument_instruction)
                        if old_part.subs_replace and i==len(old_part.sub_part_names)-1:
                            # if this is the past sub part and it's replacing the old master, then specify that, and don't append it
                            bottom_part = sub_part
                            # TO DO EVENTUALLY... BAD BAD HACK!
                            sub_part.first_item = bottom_part[0]
                        else:
                            align_command = indicatortools.LilyPondCommand("set Staff.alignAboveContext = #\"" + compound_part_name + "\"", "before")
                            attach(align_command, sub_part[0])
                            compound_countainer.append(sub_part)
                    
                    bottom_container = Container()
                    bottom_container.extend(sub_part)
                    compound_countainer.append(bottom_container)

                    self.parts[compound_part_name].append(compound_countainer)

                else:
                    self.parts[compound_part_name].is_compound = True

        self.parts_prepared = True


    def make_pdf(self, subfolder = None, part_names = None, fill_skips=False, hide_empty=False):
        """
        similar to abjad's builtin show()... but uses bubble-specific file path/name instead of the abjad default,
        creates and returns pdf filename without showing it, and pdf file name does NOT increment
        """
        self.make_score()

        # if fill_skips:
        #     scoretools.append_spacer_skips_to_underfull_measures_in_expr(self)

        if part_names is not None:
            bubble = self.make_fragment_bubble(part_names)
        else:
            bubble = self

        lilypond_file = bubble.make_lilypond_file(hide_empty=hide_empty)

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

    def show_pdf(self, part_names = None, hide_empty=False):
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

        pdf_file_path = self.make_pdf(part_names=part_names, hide_empty=hide_empty)
        systemtools.IOManager.open_file(pdf_file_path)

    def append_bubble(self, bubble, divider=False, fill_rests=False, fill_skips=True, fill_self=True):
        # TO DO... divider doesn't work (how to get different kinds of bar lengths in general?)

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

        self.prepare_parts()
        bubble.prepare_parts(existing_compound_part_names = self.compound_part_names)

        # if fill_rests:
        #     if fill_self:
        #         self.fill_empty_parts_with_rests()
        #     bubble.fill_empty_parts_with_rests()
        # if fill_skips:
        #     if fill_self:
        #         self.fill_empty_parts_with_skips()
        #     bubble.fill_empty_parts_with_skips()

        # TO DO... maybe combine this with the loop below... should be no reason to loop through all the parts twice
        # OR .... combine with prepare parts (makes the most sense)
        if bubble.free:
            bubble.show_x_time = not self.ends_free
            bubble.x_time_signatures()

        # ????DOES THIS WORK OUT?
        for part_name in bubble.parts:
            if part_name not in self.parts:
                self.parts[part_name] = bubble.parts[part_name]

        for part_name in self.parts:
            if part_name in bubble.parts:
                if len(bubble.time_signatures) > 0 and len(self.time_signatures) > 0 and len(bubble.parts[part_name]) > 0 and bubble.time_signatures[0] != self.time_signatures[-1]:
                    # time signatures attached to staff are not copied over with extend... 
                    # so attach bubble's time signature to the music inside the staff
                    # first so that it is copied 
                    
                    # if odd meters, then the time signatures are already in the measures...

                    if bubble.odd_meters and not bubble.free:
                        attach(copy.deepcopy(bubble.time_signatures[0]), bubble.parts[part_name])

            
                self.parts[part_name].append_part(bubble.parts[part_name])


        self.measures_durations += bubble.measures_durations
        self.time_signatures += bubble.time_signatures
        self.ends_free = bubble.free







    def pdf_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.pdf_path + "/" + subfolder + self.project.name + "-" + self.name + ".pdf"

    def ly_path(self, subfolder=None):
        subfolder = subfolder + "/" if subfolder is not None else ""
        return self.project.ly_path + "/" + subfolder + self.project.name + "-" + self.name + ".ly"




    def make_lilypond_file(self, hide_empty=False):
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

            if hide_empty:
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

            # assume we can use default dimensions...

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

            if hide_empty:
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

            with open(self.ly_path(), "w") as ly_file:
                ly_file.write(format(lilypond_file))

            return lilypond_file

