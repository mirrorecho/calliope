# import abjad, calliope
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


class Events(list):

    def __iter__(self):
        print("CALLING ITER")
        # return IterEvents(iter_on=self)
        x = 0
        while x < len(self):
            print("while loop")
            value = self[x]
            x += 1 
            yield value

    def get_events(self):
        return [y for y in self]

e = Events(('a','b','c','d','e','f','g','h'))

for b in e:
    print(b)



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







