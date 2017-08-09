import abjad

n1 = None
n2 = None

n1 = abjad.Note("as'")
n2 = abjad.Note("bs'")

abjad.show(n2)



# import abjad
# from calliope import tools, bubbles, machines

# class BaseCell(machines.Cell):
#     high = machines.Event(pitch=40, beats=2)
#     mid = machines.Event(pitch=38, beats=2)
#     low = machines.Event(pitch=33, beats=1.25)

# class CellLibrary(bubbles.Bubble):



# class MyShortScore(bubbles.Bubble):
#     is_simultaneous = True

#     line1 = machines.Line(
#         machines.Event(pitch=0, beats=1),
#         machines.Event(pitch=0, beats=1),
#         )
#     line2 = machines.Line(
#         machines.Event(pitch=2, beats=1),
#         machines.Event(pitch=2, beats=1),
#         )
#     line3 = machines.Line(
#         machines.Event(pitch=4, beats=1),
#         machines.Event(pitch=4, beats=1),
#         )
#     line4 = machines.Line(
#         machines.Event(pitch=5, beats=1),
#         machines.Event(pitch=5, beats=1),
#         )

# SCORE = MyShortScore()

# my_map = bubbles.Mapping() \
#     ["line1"][0, 1]() \
#     ["line3"][:]() \

# my_phrase = SCORE.map_to(machines.Phrase, my_map
#     )

# print(my_phrase[0])


# # c = b.map_to(bubbles.Bubble, bubbles.Mapping()
# #     [0]()
# #     [2]()
# #     )

# # print(b.ly)