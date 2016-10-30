from calliope import bubbles

class BubbleSequence(bubbles.Bubble):
    sequenced_bubbles = ()
    is_simultaneous = False

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble in self.sequenced_bubbles:
            my_music.append(bubble.blow())
        return my_music


class LineSequence(BubbleSequence, bubbles.Line):
    pass




