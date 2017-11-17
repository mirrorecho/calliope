import abjad, calliope
# # from calliope.sandbox import module_0, module_a


# class IterEvents(object):
#     iter_on = None
#     curr = 0

#     def __init__(self, iter_on):
#         self.iter_on = iter_on

#     def __next__(self):
#         if len(self.iter_on) <= self.curr:
#             raise StopIteration
#         else:
#             value = self.iter_on[self.curr]
#             self.curr += 1 
#             return value


class PhraseI(calliope.Phrase):
    class CellA(calliope.Cell):
        set_rhythm =  (1, 1, 0.5, 0.5)
        set_pitches = (2, 4, 5,   7)
    class CellB(calliope.Cell):
        set_rhythm =  (2, 2, 0.25, 0.25, 0.5)
        set_pitches = (2, 4, 5,    7,    9)
    class CellC(calliope.Cell):
        set_rhythm =  (1, -1, 1, -1, 1)
        set_pitches = (2, None, 5, None, 9)


p = PhraseI()

# p.non_rest_events.setattrs(beats=4)
# print( len(c.events["event_i", "sdfsfdsdfsdf", "event_ii"]) )
# c.events[:1].tag(">")
special_events = p.events[2:-2].exclude(1)
special_events.tag(">")
# special_events(pitch=4).tag(">")
special_events.tag(".")
special_events.exclude(0,2,3,-1).untag(".")

# print(len(p.cells[:-1].events))
# special_events[0,1,-1].tag(">")
# special_events[0,1].untag(">")
# p.cells[:-1].events
# p.events[1,2,-1].tag("f")

# print( type( p.select(name__in=("CellA", "CellC"))[1] ) )

p.illustrate_me()

# class SimpleScore(calliope.Score):

#     class Flute(calliope.Staff):
#         instrument=abjad.instrumenttools.Flute(
#             instrument_name="Flute", short_instrument_name="fl.")

#     class Clarinet(calliope.Staff):
#         instrument=abjad.instrumenttools.ClarinetInBFlat(
#             instrument_name="Clarinet in Bb", short_instrument_name="cl.")

#     class StringsStaffGroup(calliope.StaffGroup):
#         class Violin(calliope.Staff):
#             instrument=abjad.instrumenttools.Violin(
#                 instrument_name="Violin", short_instrument_name="vln.")

#         class Cello(calliope.Staff):
#             instrument=abjad.instrumenttools.Violin(
#                 instrument_name="Cello", short_instrument_name="vc.")
#             yo = calliope.Fragment(
#                 music_contents = "c1 d1",
#                 clef = "bass"
#                 )

# short_score = calliope.MatchSequence(
#     calliope.Bubble.from_module(module_0, name="section_0"),
#     calliope.Bubble.from_module(module_a, name="section_a"),
# )

# TO DO: something like this should work:
# short_score["section_0"].append(calliope.Fragment("e''2", name="Clarinet"))

# short_score_inverted = short_score.get_inverted()
# print(short_score_inverted.ly())

# calliope.illustrate_me(score_type=SimpleScore, bubble=short_score())







