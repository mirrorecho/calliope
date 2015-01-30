from abjad import *

import copy



# TO DO... could also pass note as pitch object
def get_pitch_number(pitch_object):
    if isinstance(pitch_object, int):
        return pitch_object
    elif isinstance(pitch_object, str):
        return pitchtools.NamedPitch(pitch_object).pitch_number
    elif isinstance(pitch_object, pitchtools.Pitch):
        return pitch_object.pitch_number
    # TO DO... error handling here?

def get_pitch_range(low_pitch, high_pitch):
    return pitchtools.PitchRange("[" + str(get_pitch_number(low_pitch)) + ", " + str(get_pitch_number(high_pitch)) + "]")

def get_music_container(music_object):
    if isinstance(music_object, scoretools.Container):
        return music_object
    else:
        return scoretools.Container(music_object)

def get_pitch_ranges(
            num_lines=1,
            low_pitches=[0],
            high_intervals=[11],
            increments=[[1]],
            times=24,
            ):
    pitch_ranges=[]
    if num_lines == 0:
        print("Warning... trying to get pitch ranges for 0 lines!")
    else:
        for l in range(num_lines):
            pitch_range = []
            low_pitch=get_pitch_number(low_pitches[l % len(low_pitches)])
            high_pitch=low_pitch+high_intervals[l % len(high_intervals)]
            increments_line=increments[l % len(increments)]
            for c in range(times):
                pitch_range.append(get_pitch_range(
                    low_pitch,
                    high_pitch,
                    ))
                increment=increments_line[c % len(increments_line)]
                low_pitch+=increment
                high_pitch+=increment
            pitch_ranges.append(pitch_range)
    return pitch_ranges
    

def transpose_pitches(pitch_stuff, transpose):
    if isinstance(pitch_stuff, (list, tuple)):
        return [transpose_pitches(p, transpose) for p in pitch_stuff]
    else:
        return get_pitch_number(pitch_stuff) + transpose

def pitches_from_intervals(intervals, start_pitch=0):
    """
    takes a start pitch and list of intervals, and returns a list of pitch numbers
    """
    start_pitch_number = get_pitch_number(start_pitch)
    return [get_pitch_number(sum(intervals[:x+1])) + start_pitch_number for x in range(len(intervals))]


# TO DO: add transpose, and spelling here! (also, could add auto-spelling)
def music_from_durations(durations, times=None, split_durations=None, pitches=None, transpose=0, respell=None, pitch_offset=0):
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
        for i, note_or_tied_notes in enumerate(iterate(music).by_logical_tie(pitched=True)):
            #QUESTION... should we NOT loop around the pitches?
            pitch_stuff = pitches[(i+pitch_offset) % len(pitches)]
            for note in note_or_tied_notes:
                # assuming everyting in the logical tie is a note than can be transposed...
                if isinstance(pitch_stuff, (list, tuple)):
                    # make a cord, if it's a list or tuple
                    chord_index = music.index(note)
                    written_duration = copy.deepcopy(note.written_duration)
                    music.remove(note)
                    chord = Chord()
                    chord.note_heads = [get_pitch_number(p) + transpose for p in pitch_stuff]
                    chord.written_duration = written_duration
                    music.insert(chord_index, chord)
                elif pitch_stuff == "x":
                    note.written_pitch = 0
                    x_notes_on = indicatortools.LilyPondCommand('xNotesOn', 'before')
                    x_notes_off = indicatortools.LilyPondCommand('xNotesOff', 'after')
                    attach(x_notes_on, note)
                    attach(x_notes_off, note)
                else:
                    note.written_pitch = get_pitch_number(pitch_stuff) + transpose

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
    
    #
    if respell == "flats":
        mutate(music).respell_with_flats()
    elif respell == "sharps":
        mutate(music).respell_with_sharps()
    elif respell == "auto":
        print("AUTO RESPELL NOT SUPPORTED YET...")
    
    return music


def attach_commands(commands, music_object):
    for c in commands:
        attach(c, music_object)


def line_staff_skip(skip_length=(1,16)):

    #skip = scoretools.Skip(skip_length)
    
    skip1 = scoretools.Skip((skip_length[0], skip_length[1]*2))
    skip2 = scoretools.Skip((skip_length[0], skip_length[1]*2))

    line_staff_commands = [
        indicatortools.LilyPondCommand("stopStaff", 'before'),
        indicatortools.LilyPondCommand("""override Staff.StaffSymbol #'line-positions = #'(
        -0.4 -0.3 -.2 -.1 0 .1 .2 .3 .4
        ;-0.5 0
        )""", 'before'),
        indicatortools.LilyPondCommand("startStaff", 'before'),
    ]

    normal_staff_commands = [
        indicatortools.LilyPondCommand("stopStaff", 'after'),
        indicatortools.LilyPondCommand("override Staff.StaffSymbol #'line-positions = #'(-4 -2 0 2 4)", 'after'),
        indicatortools.LilyPondCommand("startStaff", 'after'),
    ]

    attach_commands(line_staff_commands, skip1)
    attach_commands(normal_staff_commands, skip2)
    skip_container = Container()
    skip_container.append(skip1)
    skip_container.append(skip2)

    return skip_container

# adds the box marks (sans the single line staff before/after)
def make_box_marks(music_start_item, music_end_item):
    box_start_commands = [
        indicatortools.LilyPondCommand("once \\override BreathingSign #'break-align-symbol = #'custos", 'before'),
        indicatortools.LilyPondCommand("""once \\override Staff.TimeSignature.space-alist =
            #'((first-note . (fixed-space . 2.0))
               (right-edge . (extra-space . 0))
               ;; space after time signature ..
               (custos . (extra-space . 0)))""", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'text = \\markup { \\filled-box #'(0 . 0.4) #'(-1.4 . 1.4) #0 }", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'break-visibility = #end-of-line-invisible", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'Y-offset = ##f", 'before'),
        indicatortools.LilyPondCommand("once \\override Staff.BarLine #'space-alist = #'((breathing-sign fixed-space 0))", 'before'),
        indicatortools.LilyPondCommand("breathe", 'before'),
        ]
    box_stop_commands = [
        indicatortools.LilyPondCommand("once \\override BreathingSign #'text = \markup { \\filled-box #'(0 . 0.4) #'(-1.4 . 1.4) #0 }", 'after'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'Y-offset = ##f", 'after'),
        indicatortools.LilyPondCommand("breathe", 'after'),
    ]
    attach_commands(box_start_commands, music_start_item)
    attach_commands(box_stop_commands, music_end_item)

# can live with this for now... but would be nicer to avoid having to use skips
def box_music(music, line_before_length=(1,16), line_after_length=(1,16)):
    music = get_music_container(music)
    music_selection = music.select_leaves()
    if len(music_selection) > 0:
        return_music = Container()
        return_music.append(line_staff_skip(line_before_length))
        make_box_marks(music_selection[0], music_selection[-1])
        return_music.extend(music)
        return_music.append(line_staff_skip(line_after_length))
        return return_music
    else:
        print("Error... tried to create a box around empty music")


