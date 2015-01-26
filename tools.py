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