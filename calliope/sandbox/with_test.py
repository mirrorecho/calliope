import abjad
import time

timer = abjad.Timer()
with timer:
    for i in range(2000000):
            print(i)
print(f'total time: {timer.elapsed_time}')
