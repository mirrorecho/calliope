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
    elif isinstance(pitch_object, (list, tuple)):
        return [get_pitch_number(p) for p in pitch_object]
    # TO DO... error handling here?

def get_pitch_hz(pitch):
    return 261.6 * (2**( get_pitch_number(pitch) /12))

def get_pitch_range(low_pitch, high_pitch):
    return pitchtools.PitchRange("[" + str(get_pitch_number(low_pitch)) + ", " + str(get_pitch_number(high_pitch)) + "]")

def get_music_container(music_object):
    if isinstance(music_object, scoretools.Container):
        return music_object
    if isinstance(music_object, (list, tuple)):
        c = Container()
        for i in music_object:
            c.extend(get_music_container(i))
        return c
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
def music_from_durations(durations, times=None, split_durations=None, pitches=None, 
    transpose=0, respell=None, pitch_offset=0, pitch_columns=None):
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
            if pitch_columns is not None:
                p_i = pitch_columns[i % len(pitch_columns)]
            else:
                p_i = i
            pitch_stuff = pitches[(p_i+pitch_offset) % len(pitches)]
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

# TO DO... auto find best harmonic?
# TO DO.... make this!
def make_harmonics(music, 
            show_pitch_indices=[None], # none shows all
            harmonic_types=["artificial"], 
            # all these have to do with natural harmonics:
            harmonics=[None],
            max_partial = 5 ,
            positions = [1],
            strings=["G3"]):

    if type(music) is str:
        music = scoretools.Container(music)
    # ASSUME THE COPY ISN'T NEEDED
    # elif isinstance(durations, scoretools.Container):
    #     music = copy.deepcopy(durations)

    for i, note_or_tied_notes in enumerate(iterate(music).by_logical_tie(pitched=True)):
        # TO DO EVENTUALLY do we even need this double loop here??
        for note in note_or_tied_notes:
            # assuming everyting in the logical tie is a note than can be transposed...
            
            harmonic_type = harmonic_types[i % len(harmonic_types)]
                        
            if show_pitch_indices[0] is None or i in show_pitch_indices:
                show_sound_pitch = True
            else:
                show_sound_pitch = False

            sound_pitch = note.written_pitch
            duration = copy.deepcopy(note.written_duration) # is this copy needed?
            chord_index = music.index(note)

            if harmonic_type == "artificial":
                # override(note).note_head.style = 'harmonic'

                music.remove(note)

                chord = Chord()
                chord.note_heads = [sound_pitch-24, sound_pitch-19]
                chord.note_heads[1].tweak.style = "harmonic"
                chord.written_duration = duration

                if show_sound_pitch:
                    chord.note_heads.append(sound_pitch)
                    chord.note_heads[2].tweak.font_size = -3
                music.insert(chord_index, chord)

            else:

                harmonic = harmonics[i % len(harmonics)]
                string = strings[i % len(strings)]
                position = positions[i % len(positions)]

                show_string_instruction = True

                if harmonic is None:
                    string_pitch = get_pitch_number(string)
                    string_hz = get_pitch_hz(string)

                    for h in range(max_partial):
                        # try the higher harmonics first (lower finger positions)
                        fundamendal_hz = get_pitch_hz(sound_pitch) / (max_partial - h)
                        # have to convert back to pitch #s, for comparison since there may be minor discrepancies due to tuning
                        fundamendal_pitch = pitchtools.NumberedPitch.from_hertz(fundamendal_hz)
                        if fundamendal_pitch == string_pitch:
                            harmonic = max_partial - h
                            break

                if harmonic is None:
                    print("ERROR: could not find natural harmonic for pitch " + pitchtools.NamedPitch(sound_pitch).pitch_class_octave_label  + "through partial #" + str(max_partial) + " on string " + string)
                else:
                    print(harmonic)
                    finger_hz = string_hz * harmonic / (harmonic - position)
                    finger_pitch = pitchtools.NumberedPitch.from_hertz(finger_hz).pitch_number
                    if finger_pitch == sound_pitch:
                        show_sound_pitch = False



                    if show_sound_pitch:
                        music.remove(note)
                        chord = Chord()
                        chord.note_heads = [finger_pitch, sound_pitch]
                        chord.note_heads[0].tweak.style = "harmonic"
                        chord.note_heads[1].tweak.font_size = -3
                        chord.written_duration = duration
                        if show_string_instruction:
                            string_instruction = markuptools.Markup(string[0] + " string", direction=Up)
                            attach(string_instruction, chord)
                        music.insert(chord_index, chord)
                    else:
                        override(note).note_head.style = "harmonic"
            print("made harmonic")
    return music



def attach_commands(commands, music_object):
    for c in commands:
        attach(c, music_object)


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

def hidden_leaf(length=(1,4), pitch=None):
    if pitch == None:
        leaf = scoretools.Rest(length)
    else:
        leaf = scoretools.Note(pitch, length)
    hide_notes = indicatortools.LilyPondCommand("hideNotes", 'before')
    unhide_notes = indicatortools.LilyPondCommand("unHideNotes", 'after')
    attach(hide_notes, leaf)
    attach(unhide_notes, leaf)
    return leaf

def continue_arrow():
    arrow_commands = [
            indicatortools.LilyPondCommand("once \override Rest  #'stencil = #ly:text-interface::print", "before"),
            indicatortools.LilyPondCommand("once \override Rest.staff-position = #-2.2", "before"),
            indicatortools.LilyPondCommand("once \override Rest #'text = \\markup { \\fontsize #6 { \\general-align #Y #DOWN { \\arrow-head #X #RIGHT ##t } } }" , "before"),
            ]
    rest_arrow = scoretools.Rest((1,16))
    attach_commands(arrow_commands, rest_arrow)
    return rest_arrow


def staff_line_commands(lines=(-4, -2, 0, 2, 4), command_position="after"):
    commands = []
    commands.append(indicatortools.LilyPondCommand("stopStaff", command_position))
    commands.append(indicatortools.LilyPondCommand(
                "override Staff.StaffSymbol #'line-positions = #'(" + " ".join([str(i) for i in lines]) + ")", 
                command_position))
    commands.append(indicatortools.LilyPondCommand("startStaff", command_position))
    return commands


def line_staff_skip(position="grace", continue_staff=False):

    #skip = scoretools.Skip(skip_length)
    
    before_staff_line_skip = hidden_leaf((1,32))
    before_staff_normal_skip = hidden_leaf((1,16))

    attach_commands(staff_line_commands((-0.4, -0.3, -.2, -.1, 0, .1, .2, .3, .4)), before_staff_line_skip)
    attach_commands(staff_line_commands(()), before_staff_normal_skip)

    skip_container = scoretools.GraceContainer(kind=position)
    skip_container.append(before_staff_line_skip)    
    if not continue_staff:
        skip_container.append(before_staff_normal_skip)
    return skip_container

def line_staff_continue(continue_lengths):
    # (we're assuming that the staff has already been converted to a line)
    line_container = Container()
    for d in continue_lengths:

        # append a hidden leaf for the first half of the continue line for this duration
        half_continue = (d[0], d[1]*2)
        line_container.append(hidden_leaf(half_continue))

        # now make a hidden leaf for the second half, but attach an arrow to the beginning of it
        # also the 2nd hidden leaf is a NOTE (not a rest)... that way lines will never be hidden
        half_continue_leaf2 = hidden_leaf(half_continue, 0)
        arrow_container = scoretools.GraceContainer()
        arrow_container.append(continue_arrow())
        attach(arrow_container, half_continue_leaf2)
        # now append the leaf for the second half (with the arrow)
        line_container.append(half_continue_leaf2)

    # now return the staff to normal
    attach_commands(staff_line_commands(()), line_container[-1] )
    
    return line_container



# can live with this for now... but would be nicer to avoid having to use skips
def box_music(music, instruction=None, continue_lengths=None):
    music = get_music_container(music)
    music_selection = music.select_leaves()
    if len(music_selection) > 0:

        attach(line_staff_skip(), music_selection[0])

        if instruction is not None:
            instruction_markup = markuptools.Markup('\italic { "' + instruction + '" }', direction=Up)
            attach(instruction_markup, music_selection[0])

        continue_line_staff = False if continue_lengths is None else True

        attach(line_staff_skip(position="after", continue_staff=continue_line_staff), music_selection[-1])

        if continue_line_staff:
            music.extend(line_staff_continue(continue_lengths))

        return music


        # return_music = Container()
        # padding_div_length=(padding_length[0],padding_length[1]*4)
        
        # return_music.append(hidden_leaf(padding_div_length))
        # return_music.append(line_staff_skip())

        # make_box_marks(music_selection[0], music_selection[-1])
        # return_music.extend(music)
        
        # return_music.append(line_staff_skip())
        # return_music.append(hidden_leaf(padding_div_length))


        # return return_music

    else:
        print("Error... tried to create a box around empty music")

# TO DO EVENTUALLY... replace by class... also replace within music?
def replace_pitch(pitch_stuff, pitch, other_pitch):
    if isinstance(pitch_stuff, (list, tuple)):
        return [replace_pitch(p, pitch, other_pitch) for p in pitch_stuff]
    else:
        if get_pitch_number(pitch) == get_pitch_number(pitch_stuff):
            return get_pitch_number(other_pitch)
        else:
            return get_pitch_number(pitch_stuff)
