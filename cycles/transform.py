from abjad import *
from calliope.cycles.cells import IntervalRepeatCell
from calliope.cloud.pitches import CloudPitches
from calliope.tools import get_pitch_number, music_from_durations, transpose_pitches

import copy

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

class AddMaterial(TransformBase):
    def apply(self, cycle, previous_cycle):
        if "material_type" in self.args: 
            cycle.material[self.args["material_type"]][self.name] = self.args["value"]
        else:
            cycle.material[self.name] = self.args["value"]

class ArrangeMusic(TransformBase):
    def apply(self, cycle, previous_cycle):
        cycle.arrange_music(**self.args)

class ExecMethod(TransformBase):
    def apply(self, cycle, previous_cycle):
        method = getattr(cycle, self.name)
        method(**args)

class ModAddPoint(TransformBase):
    """
    adds a number to a sorted list (and resorts). 
    useful for building up rhythmic patterns
    """
    #TO DO... test if material is list?
    def apply(self, cycle, previous_cycle):
        cycle.material[self.name] = cycle.material[self.name].copy()
        cycle.material[self.name].append(self.args["point"])
        cycle.material[self.name].sort()

class MakeMusicFromHits(TransformBase):
    # name = name of hits material to use
    # parts
    # pitches = pitch stack... should be same length as parts, in same order
    # denominator
    # cycle_length
    # ... currently assumes that pitches stay the same for each hit in the cycle
    # ... and that no other music added in the cycle for any of these parts...
    def apply(self, cycle, previous_cycle):
        talea = []
        hits = cycle.material[self.name]
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
            cycle.arrange_music(durations=durations, **self.args)
            # SHOULD NOT NEED THIS...
            # for part_name, pitch in zip(self.args["part_names"], cycle.data[self.args["pitches"]]):
            #     music = music_from_durations(
            #                     durations=durations, 
            #                     split_durations=cycle.measures_durations, 
            #                     pitches=[pitch])
            #     cycle.arrange_music(part_name, music)


class ArrangeMusicFromIntervalRepeatCell(TransformBase):
    def apply(self, cycle, previous_cycle):
        pitch_range = None
        if "pitch_range" in self.args:
            pitch_range = cycle.material[self.args["pitch_range"]]
        cell = IntervalRepeatCell(cycle.material[self.args["intervals"]], cycle.material[self.args["start_pitch"]], pitch_range=pitch_range)
        pitches = []
        for i in range(self.args["times"]):
            pitches.extend(cell.pitches())
            cell.next()
        cycle.arrange_music(pitches=[self.pitches], **self.args)

class AddPitchMaterialFromIntervalRepeatCell(TransformBase):
    def apply(self, cycle, previous_cycle):
        pitch_range = None
        if "pitch_range" in self.args:
            pitch_range = cycle.material[self.args["pitch_range"]]
        cell = IntervalRepeatCell(intervals=cycle.material[self.args["intervals"]], start_pitch=cycle.material[self.args["start_pitch"]][0], pitch_range=pitch_range)
        cycle.material[self.name] = []
        for i in range(self.args["times"]):
            cycle.material[self.name].extend(cell.pitches)
            cell.next()

class ModTransposePitch(TransformBase):
    def apply(self, cycle, previous_cycle):
        if previous_cycle is not None:
            previous_pitch = previous_cycle.material["pitch"][self.name]
            new_pitch = transpose(previous_pitch, self.args["value"])
            cycle.material["pitch"][self.name] = new_pitch


# TO DO... necessary?

# -------------------------------------------------------------------------------
# class CopyPitchMaterial(TransformBase):
#     def apply(self, cycle, previous_cycle):
#         copy_from = cycle.data[self.args["copy_from"]]
#         transpose = 0
#         if "transpose" in self.args:
#             transpose = cycle.data[self.args["transpose"]]
#         if "copy_to_names" in self.args:
#             if isinstance(transpose, list):
#                 for copy_to_name, transpose_value in zip(self.args["copy_to_names"], transpose):
#                     cycle.data[copy_to_name] = [get_pitch_number(pitch) + transpose_value for pitch in copy_from]
#             else:
#                 for copy_to_name in self.args["copy_to_names"]:
#                     cycle.data[copy_to_name] = [get_pitch_number(pitch) + transpose for pitch in copy_from]
#         else:
#             cycle.data[self.name] = [get_pitch_number(pitch) + transpose for pitch in copy_from]


# class CopyMusic(TransformBase):
#     def apply(self, cycle, previous_cycle):
#         music = copy.deepcopy(cycle.data[self.args["copy_from"]])
#         if "transpose" in self.args:
#             # QUESTION... does this work for chords or to they need to be handled separately?
#             for i, note in enumerate(iterate(music).by_class(Note)):
#                 note.written_pitch += cycle.data[self.args["transpose"]]
#         # if a part is specified, then add the music to that... otherwise add it to the data defined by this transform name
#         if "part" in self.args:
#             cycle.arrange_music(self.args["part"], music)
#         else:
#             cycle.data[self.name] = music

# THIS WORKS MUCH BETTER WHEN RUN AHEAD OF TIME AND THEN LOADED INTO THE BUBBLE CLASS AS PITCH MATERIAL
# class ModCloudPitchesRearrangeLines(TransformBase):
#     # tally_apps
#     # times 
#     # pitch_lines 
#     def apply(self, cycle, previous_cycle):
#         pitch_lines = cycle.data[self.name]
#         # assume we don't need the project, since we won't be showing anything directly...
#         cloud = CloudPitches(pitch_lines=pitch_lines)
#         cloud.randomize_all_columns()
#         for tally_app in self.args["tally_apps"]:
#             cloud.add_tally_app(tally_app)
#         for i in range(self.args["tally_times"]):
#             cloud.get_tallies()
#             cloud = cloud.get_rearranged()


# class MakePitchLines(TransformBase):
#     def apply(self, cycle, previous_cycle):
#         # create a new list if not already created:
#         if self.name not in cycle.data:
#             cycle.data[self.name] = []
#         copy_from = cycle.data[self.args["copy_from"]]
#         harmonic_stack = cycle.data[self.args["harmonic_stack"]]
#         for i, transpose in enumerate(harmonic_stack):
#             new_line = [get_pitch_number(pitch) + transpose for pitch in copy_from]
#             cycle.data[self.name].append(new_line)

# class CopyPitch(TransformBase):
#     def apply(self, cycle, previous_cycle):
#         transpose = 0
#         if "transpose" in self.args:
#             transpose = cycle.data[self.args["transpose"]]
#         cycle.data[self.name] = pitchtools.NumberedPitch(cycle.data[self.args["copy_from"]] + transpose)



