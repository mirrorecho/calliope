from copy import deepcopy
from abjad import * # TO DO... kill this
import abjad

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

def remove_pitch_repetitions(pitch_row):
    ret_row = []
    for i, p in enumerate(pitch_row):
        if i == 0 or get_pitch_number( p ) != get_pitch_number( pitch_row[i-1] ):
            ret_row.append(p)
    return ret_row


def get_pitch_hz(pitch):
    return 261.6 * (2**( get_pitch_number(pitch) /12))

def get_pitch_range(low_pitch, high_pitch):
    return pitchtools.PitchRange("[" + str(get_pitch_number(low_pitch)) + ", " + str(get_pitch_number(high_pitch)) + "]")

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
def set_pitches(music, pitches=None, transpose=0, offset=0, indices=None, pitch_range=None):
    # TO DO... transpose should use real transpose interval!

    if pitches is not None:
        for i, note_or_tied_notes in enumerate(iterate(music).by_logical_tie(pitched=True)):

            if indices is not None:
                p_i = indices[i % len(indices)]
            else:
                p_i = i

            #QUESTION... should we NOT loop around the pitches?
            pitch_stuff = pitches[(p_i+offset) % len(pitches)]

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
                    x_notes_on = abjad.LilyPondCommand('xNotesOn', 'before')
                    x_notes_off = abjad.LilyPondCommand('xNotesOff', 'after')
                    attach(x_notes_on, note)
                    attach(x_notes_off, note)
                else:
                    note.written_pitch = get_pitch_number(pitch_stuff) + transpose

                if pitch_range is not None:
                    note.written_pitch = pitchtools.transpose_pitch_expr_into_pitch_range([note.written_pitch.pitch_number], pitch_range)[0]


def respell(music, respell="auto"):
    if respell == "flats":
        mutate(music).respell_with_flats()
    elif respell == "sharps":
        mutate(music).respell_with_sharps()
        # print("RESPELLING WITH SHARPS")
    elif respell == "auto":
        print("AUTO RESPELL NOT SUPPORTED YET...")


# TO DO EVENTUALLY... replace by class... also replace within music?
def replace_pitch(pitch_stuff, pitch, other_pitch):
    if isinstance(pitch_stuff, (list, tuple)):
        return [replace_pitch(p, pitch, other_pitch) for p in pitch_stuff]
    else:
        if get_pitch_number(pitch) == get_pitch_number(pitch_stuff):
            return get_pitch_number(other_pitch)
        else:
            return get_pitch_number(pitch_stuff)


# TO DO... auto-find best harmonic?
# TO DO.... make this!
def string_harmonics(music, 
            show_pitch_indices=(None,), # none shows all
            harmonic_types=["artificial"], 
            # all these have to do with natural harmonics:
            harmonics=(None,),
            max_partial = 5 ,
            positions = [1],
            strings=["G3"]):
    """
    auto-generates indications for string harmonics
    """

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
            duration = deepcopy(note.written_duration) # is this copy needed?
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

            elif harmonic_type == "natural":

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
                    # print(harmonic)
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
            # print("made harmonic")
    # return music