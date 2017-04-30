import abjad
from calliope import bubbles, tools

def every(start=0, end=2, every_count=2):
    slurs_data = ID()
    for i in range(start, end, every_count):
        slurs_data[i] = "("
        slurs_data[i+every_count-1] = ")"
    return slurs_data