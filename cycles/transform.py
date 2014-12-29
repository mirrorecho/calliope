from abjad import *
from calliope.cycles.cells import IntervalRepeatCell
from calliope.cloud.pitches import CloudPitches

import copy

# TO DO... make sure using pitches as numbers everywhere...

def get_pitch_number(pitch_object):
    if isinstance(pitch_object, int):
        return pitch_object
    elif isinstance(pitch_object, str):
        return pitchtools.NamedPitch(pitch_object).pitch_number
    elif isinstance(pitch_object, pitchtools.Pitch):
        return pitch_object.pitch_number

def music_from_durations(durations, times=None, split_durations=None, pitches=None):
    # durations is either:
    # - a string with rests and notes (usually c) to be transposed by pitches
    # - a music container with rests and notes (usually c) to be transposed by pitches
    # a list of durations
    if type(durations) is str:
        music = scoretools.Container(durations)
    elif isinstance(durations, scoretools.Container):
        music = copy.deepcopy(durations)
    else:
        # should durations also be copied here???
        music = scoretools.make_leaves([0], durations)

    if pitches is not None:
        for i, note in enumerate(iterate(music).by_class(Note)):
            #QUESTION... should we NOT loop around the pitches?
           note.written_pitch += get_pitch_number(pitches[i % len(pitches)])

    if times is not None:
        music_times = scoretools.Container()
        for i in range(times):
            music_times.extend(copy.deepcopy(music))
        music = music_times

    # split notes accross bar lines (with ties) .... 
    if split_durations is not None:
        music = mutate(music).split(
                        split_durations,
                        fracture_spanners=False,
                        tie_split_notes=True,
                        )
    return music


class TransformBase:

    name = ""

    start_flag = None
    stop_flag = None
    start_iter = None # the cycle iteration to start on... if negative, will count from the end (e.g. -1 will start on the last cycle, -2 on the second to last)
    stop_iter = None # the cycle iteration to stop on... likewise, if negative, will count from the end
    apply_flags = []
    
    is_loop_active = False

    args = {}

    def __init__(self, name=None, stop_flag=None, start_flag=None, start_iter=None, stop_iter=None, apply_flags=[], skip_flags=[], **kwargs):
        self.name = name
        
        self.start_flag = start_flag
        self.stop_flag = stop_flag
        self.start_iter = start_iter
        self.stop_iter = stop_iter
        self.apply_flags = apply_flags
        self.skip_flags = skip_flags

        # TO DO... add skip flags?

        # if no start is specified, start at 0:
        if start_iter is None and start_flag is None and len(apply_flags) == 0:
            self.start_iter = 0

        self.args = kwargs

    def is_active(self, loop_iter, loop_total, flags):
        # make "loop inactive" if this cycle is flagged with the loop stop flag or iteration 
        # (note we give priority to stopping over starting... if they ever both apply)
        if (
            self.stop_flag in flags or 
            loop_iter == self.stop_iter or 
            (self.stop_iter is not None and self.stop_iter < 0 and loop_iter == self.stop_iter + loop_total)
        ):
            self.is_loop_active = False
        # otherwise make "loop active" if this cycle is flagged with the loop start flag or iteration 
        elif (
            self.start_flag in flags or 
            loop_iter == self.start_iter or 
            (self.start_iter is not None and self.start_iter < 0 and loop_iter == self.start_iter + loop_total)
        ):
            self.is_loop_active = True        

        return ((
                    self.is_loop_active 
                    or any(f in self.apply_flags for f in flags)
                ) 
                and not any(f in self.skip_flags for f in flags)
                ) 


    def apply(self, cycle, previous_cycle):
        pass

# something to think about ...

# class ArrangementProperties():
#     part_name = None
#     before_durations = None
#     durations = None
#     after_durations = None
#     transposition = 0

class AddData(TransformBase):
    def apply(self, cycle, previous_cycle):
        cycle.data[self.name] = self.args["value"]


class MakeMusic(TransformBase):
    def apply(self, cycle, previous_cycle):
        if "pitches" in self.args:
            pitches = [get_pitch_number(p) for p in cycle.data[self.args["pitches"]]]
        elif "pitch" in self.args:
            pitches = [get_pitch_number(cycle.data[self.args["pitch"]])]
        elif "relative_pitches" in self.args and "start_pitch" in self.args:
            start_pitch = cycle.data[self.args["start_pitch"]]
            relative_pitches = cycle.data[self.args["relative_pitches"]]        
            pitches = [get_pitch_number(start_pitch) + i for i in relative_pitches]
        else:
            pitches = None

        # better to pull from cycle data instead of just passing parameter???
        if "times" in self.args:
            times=self.args["times"]
        else:
            times = None

        # split notes accross bar lines (with ties) .... QUESTION... should this happen here or at the arrangement mod?
        music = music_from_durations(
                        durations=cycle.data[self.args["durations"]], 
                        split_durations=cycle.measures_durations, 
                        pitches=pitches,
                        times=times)

        if "pitch_range" in self.args:
            # QUESTION... does this work for chords or to they need to be handled separately?
            for i, note in enumerate(iterate(music).by_class(Note)):
                note.written_pitch = pitchtools.transpose_pitch_expr_into_pitch_range([note.written_pitch.pitch_number], cycle.data[self.args["pitch_range"]])[0]
        
        # if a part is specified, then add the music to that... otherwise add it to the data defined by this transform name
        if "part" in self.args:
            cycle.arrange_music(self.args["part"], music)
        else:
            cycle.data[self.name] = music

# handles basic parameters for pitch_lines, duration/durations/durations_lines, and parts... could be extended if needed (transpose, times, pitch_ranges, etc.)
class MakeMusicLines(TransformBase):
    def apply(self, cycle, previous_cycle):
        pitch_lines = cycle.data[self.args["pitch_lines"]]
        if "duration" in self.args:
            # all pitches on all lines get the same duration:
            durations = [cycle.data[self.args["duration"]] for i in range(len(pitch_lines[0]))]
            durations_lines = [durations for i in range(len(pitch_lines))]
        elif "durations" in self.args:
            # different durations for different pitch columns (but same for each line)
            durations_lines = [cycle.data[self.args["durations"]] for i in range(len(pitch_lines))]
        elif "durations_lines" in self.args:
            # each pitch line has it's own unique line of durations
            durations_lines = cycle.data[self.args["durations_lines"]]

        if "parts" in self.args:
            for pitch_line, durations_line, part in zip(pitch_lines, durations_lines, self.args["parts"]):
                cycle.arrange_music(part, music_from_durations(
                            durations=durations_line, 
                            split_durations=cycle.measures_durations, 
                            pitches=pitch_line
                            ))
        # anything else that should be done other than copy the lines to parts?

class ArrangeAll(TransformBase):
    def apply(self, cycle, previous_cycle):
        for part_name, part in cycle.arrangement.parts.items():
            if part.is_simultaneous:
                for i in range(len(part)):
                    music = copy.deepcopy(cycle.data[self.name])
                    cycle.arrange_music(part_name=part_name, music=music, staff_number=i)
            else:
                music = copy.deepcopy(cycle.data[self.name])
                cycle.arrange_music(part_name=part_name, music=music)
            # TO DO... Hide time signature and add dotted bar line(s)



class CopyMusic(TransformBase):
    def apply(self, cycle, previous_cycle):
        music = copy.deepcopy(cycle.data[self.args["copy_from"]])
        if "transpose" in self.args:
            # QUESTION... does this work for chords or to they need to be handled separately?
            for i, note in enumerate(iterate(music).by_class(Note)):
                note.written_pitch += cycle.data[self.args["transpose"]]
        # if a part is specified, then add the music to that... otherwise add it to the data defined by this transform name
        if "part" in self.args:
            cycle.arrange_music(self.args["part"], music)
        else:
            cycle.data[self.name] = music

class MakeMusicFromHits(TransformBase):
    # name = name of hits data to use
    # parts
    # pitches = pitch stack... should be same length as parts, in same order
    # denominator
    # cycle_length
    # ... currently assumes that pitches stay the same for each hit in the cycle
    # ... and that no other music added in the cycle for any of these parts...
    def apply(self, cycle, previous_cycle):
        talea = []
        hits = cycle.data[self.name]
        if len(hits) > 0:
            cycle_length = self.args["cycle_length"]
            talea.append(0 - hits[0]) # adds initial rest (could be 0)
            for i in range(len(hits)):
                if i>0:
                    talea.append(hits[i-1] - (hits[i] - 1)) # adds rests between each note(could be 0)
                talea.append(1)
            talea.append(hits[len(hits)-1] - (cycle_length -1) ) # adds final rest (could be 0)
            talea = [t for t in talea if t!=0] # (gets rid of 0-length rests)
            durations = scoretools.Container()
            durations.extend(scoretools.make_leaves_from_talea(talea, self.args["denominator"]))
            for part_name, pitch in zip(self.args["parts"], cycle.data[self.args["pitches"]]):
                music = music_from_durations(
                                durations=durations, 
                                split_durations=cycle.measures_durations, 
                                pitches=[pitch])
                cycle.arrange_music(part_name, music)



class ModCloudPitchesRearrangeLines(TransformBase):
    # tally_apps
    # times 
    # pitch_lines 
    def apply(self, cycle, previous_cycle):
        pitch_lines = cycle.data[self.name]
        # assume we don't need the project, since we won't be showing anything directly...
        cloud = CloudPitches(pitch_lines=pitch_lines)
        cloud.randomize_all_columns()
        for tally_app in self.args["tally_apps"]:
            cloud.add_tally_app(tally_app)
        for i in range(self.args["tally_times"]):
            cloud.get_tallies()
            cloud = cloud.get_rearranged()

class AddMusicFromIntervalRepeatCell(TransformBase):
    def apply(self, cycle, previous_cycle):
        pitch_range = None
        if "pitch_range" in self.args:
            pitch_range = cycle.data[self.args["pitch_range"]]
        cell = IntervalRepeatCell(cycle.data[self.args["intervals"]], cycle.data[self.args["start_pitch"]], pitch_range)
        durations =cycle.data[self.args["durations"]]
        cycle.data[self.name] = scoretools.Container()
        for i in range(self.args["times"]):
            cycle.data[self.name].extend(cell.make_notes(durations))
            cell.next()

class AddPitchesFromIntervalRepeatCell(TransformBase):
    def apply(self, cycle, previous_cycle):
        pitch_range = None
        if "pitch_range" in self.args:
            pitch_range = cycle.data[self.args["pitch_range"]]
        cell = IntervalRepeatCell(cycle.data[self.args["intervals"]], cycle.data[self.args["start_pitch"]], pitch_range)
        cycle.data[self.name] = []
        for i in range(self.args["times"]):
            cycle.data[self.name].extend(cell.pitches)
            cell.next()

class ModTransposePitch(TransformBase):
    def apply(self, cycle, previous_cycle):
        if previous_cycle is not None:
            previous_pitch = previous_cycle.data[self.name]
            new_pitch = previous_pitch.transpose(self.args["value"])
            cycle.data[self.name] = new_pitch

class ModAddPoint(TransformBase):
    """
    adds a number to a sorted list (and resorts). 
    useful for building up rhythmic patterns
    """
    #TO DO... test if data is list?
    def apply(self, cycle, previous_cycle):
        cycle.data[self.name] = cycle.data[self.name].copy()
        cycle.data[self.name].append(self.args["point"])
        cycle.data[self.name].sort()

class CopyPitches(TransformBase):
    def apply(self, cycle, previous_cycle):
        copy_from = cycle.data[self.args["copy_from"]]
        transpose = 0
        if "transpose" in self.args:
            transpose = cycle.data[self.args["transpose"]]
        if "copy_to_names" in self.args:
            if isinstance(transpose, list):
                for copy_to_name, transpose_value in zip(self.args["copy_to_names"], transpose):
                    cycle.data[copy_to_name] = [get_pitch_number(pitch) + transpose_value for pitch in copy_from]
            else:
                for copy_to_name in self.args["copy_to_names"]:
                    cycle.data[copy_to_name] = [get_pitch_number(pitch) + transpose for pitch in copy_from]
        else:
            cycle.data[self.name] = [get_pitch_number(pitch) + transpose for pitch in copy_from]

class MakePitchLines(TransformBase):
    def apply(self, cycle, previous_cycle):
        # create a new list if not already created:
        if self.name not in cycle.data:
            cycle.data[self.name] = []
        copy_from = cycle.data[self.args["copy_from"]]
        harmonic_stack = cycle.data[self.args["harmonic_stack"]]
        for i, transpose in enumerate(harmonic_stack):
            new_line = [get_pitch_number(pitch) + transpose for pitch in copy_from]
            cycle.data[self.name].append(new_line)

class CopyPitch(TransformBase):
    def apply(self, cycle, previous_cycle):
        transpose = 0
        if "transpose" in self.args:
            transpose = cycle.data[self.args["transpose"]]
        cycle.data[self.name] = pitchtools.NumberedPitch(cycle.data[self.args["copy_from"]] + transpose)



