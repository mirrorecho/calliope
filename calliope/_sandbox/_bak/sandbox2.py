import abjad

n1 = None
n2 = None

n1 = abjad.Note("as'")
n2 = abjad.Note("bs'")

abjad.show(n2)



# import abjad
# from calliope import tools, bubbles, machines

# class BaseCell(calliope.Cell):
#     high = calliope.Event(pitch=40, beats=2)
#     mid = calliope.Event(pitch=38, beats=2)
#     low = calliope.Event(pitch=33, beats=1.25)

# class CellLibrary(calliope.Bubble):



# class MyShortScore(calliope.Bubble):
#     is_simultaneous = True

#     line1 = calliope.Line(
#         calliope.Event(pitch=0, beats=1),
#         calliope.Event(pitch=0, beats=1),
#         )
#     line2 = calliope.Line(
#         calliope.Event(pitch=2, beats=1),
#         calliope.Event(pitch=2, beats=1),
#         )
#     line3 = calliope.Line(
#         calliope.Event(pitch=4, beats=1),
#         calliope.Event(pitch=4, beats=1),
#         )
#     line4 = calliope.Line(
#         calliope.Event(pitch=5, beats=1),
#         calliope.Event(pitch=5, beats=1),
#         )

# SCORE = MyShortScore()

my_map = \

my_phrase = SCORE.map_to(calliope.Phrase,  bubbles.Mapping()
    ["line1"][0, 1]()
    ["line3"][:]() 
    )

# print(my_phrase[0])


# # c = b.map_to(calliope.Bubble, bubbles.Mapping()
# #     [0]()
# #     [2]()
# #     )

# # print(b.ly)