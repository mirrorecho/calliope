import inspect
import abjad
import calliope

class Part(calliope.Score):
    transpose = 0
    # TO DO... include part-specific stylesheet

    def process_music(self, music, **kwargs):
        super().process_music(music, **kwargs)
        if self.transpose:
            abjad.mutate(music).transpose(self.transpose)