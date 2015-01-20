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
            pitch_stuff = pitches[i % len(pitches)]
            if isinstance(pitch_stuff, (list, tuple)):
                # make a cord, if it's a list or tuple
                chord_index = music.index(note)
                written_duration = copy.deepcopy(note.written_duration)
                written_pitch = note.written_pitch
                music.remove(note)
                chord = Chord()
                chord.note_heads = [get_pitch_number(p) for p in pitch_stuff]
                chord.written_duration = written_duration
                music.insert(chord_index, chord)
            elif pitch_stuff == "x":
                note.written_pitch = 0
                x_notes_on = indicatortools.LilyPondCommand('xNotesOn', 'before')
                x_notes_off = indicatortools.LilyPondCommand('xNotesOff', 'after')
                attach(x_notes_on, note)
                attach(x_notes_off, note)
            else:
                note.written_pitch = get_pitch_number(pitch_stuff)

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