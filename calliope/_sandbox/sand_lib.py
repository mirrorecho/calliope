import abjad
import calliope

LOCAL_LIB = calliope.Library(namespace="sand")


@calliope.register
def drum_hits(lib):
    c = calliope.Cell(
        rhythm=(1, -3),
        pitches=(
            (-8, -5, 2, 11,),
            "R", "R", "R")
        )
    c.events[0].tag("note_head:0:cross")
    c.events[0].tag("note_head:3:cross")
    return c


@calliope.register
def drum_hits_times(lib, times=2):
    return lib("drum_hits") * times





if __name__ == '__main__':
    print("I am a main")
    lib = calliope.Library()
    # print(_registered)

