import calliope

class PhraseBlock1(calliope.PhraseBlock):
    
    class Soprano(calliope.Phrase):
        set_pitches = (11, 12, 11, 9, 16, 16,  14,  12, 11)
        set_rhythm =  (1,  1,  1,  1, 1,  0.5, 0.5, 1,  1)

    class Alto(calliope.Phrase):
        set_pitches = (8, 9, 8, 9, 8,   9,   11, 4,   6,   8)
        set_rhythm =  (1, 1, 1, 1, 0.5, 0.5, 1,  0.5, 0.5, 1)
        respell = "sharps"

    class Tenor(calliope.Phrase):
        set_pitches = (4, 4, 2, 4, 2, 0, -1, 0, 2, 4)
        set_rhythm = (1, 1, 1, 1, 0.5, 0.5, 1,  0.5, 0.5, 1)
        clef = "bass"

    class Bass(calliope.Phrase):
        set_pitches = (-8, -3, -1, 0, -1, -3, -4, -3, -8)
        set_rhythm =  (1, 1, 1, 1, 0.5, 0.5, 1, 1, 1)
        clef = "bass"
        respell = "sharps"

class PhraseBlock2(calliope.PhraseBlock):
    
    class Soprano(calliope.Phrase):
        set_pitches = (14, 12, 11, 9, 11,  12,   14,  12, 11, 9)
        set_rhythm =  (1,  1,  1,  1, 0.5, 0.25, 0.25, 1, 1,  1)

    class Alto(calliope.Phrase):
        set_pitches = (8, 9, 8, 9,   7,   5, 4, 4)
        set_rhythm =  (1, 1, 1, 0.5, 0.5, 1, 2, 1)
        respell = "sharps"

    class Tenor(calliope.Phrase):
        set_pitches = (5, 4, 4,   2,   0, 2, -4,  -3, -4,   0)
        set_rhythm =  (1, 1, 0.5, 0.5, 1, 1,  0.5, 1,  0.5, 1)
        clef = "bass"
        respell = "sharps"

    class Bass(calliope.Phrase):
        set_pitches = (-13, -12, -10, -8, -7, -8,  -10, -8, -15)
        set_rhythm =  ( 1,   0.5, 0.5, 1,  1,  0.5, 0.5, 2,  1 )
        clef = "bass"
        respell = "sharps"

class PhraseBlock3(calliope.PhraseBlock):
    
    class Soprano(calliope.Phrase):
        set_pitches = (9, 11,  9,   7, 6, 4,   6,   7, 9, 11)
        set_rhythm =  (1, 0.5, 0.5, 1, 1, 0.5, 0.5, 1, 1, 1 )

    class Alto(calliope.Phrase):
        set_pitches = (2, 2,   3,   4, 3, 4,   3,   4,   7,   6,   4,   3)
        set_rhythm =  (1, 0.5, 0.5, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1)
        respell = "sharps"
        metrical_durations = ( ((1,4),)*4 )* 2

    class Tenor(calliope.Phrase):
        set_pitches = (-3, -5,  -3,  -1, -1, -1,  -3,  -1, 0, -6)
        set_rhythm =  ( 1,  0.5, 0.5, 1,  1,  0.5, 0.5, 1, 1,  1)
        clef = "bass"
        respell = "sharps"
        metrical_durations = ( ((1,4),)*4 )* 2

    class Bass(calliope.Phrase):
        set_pitches = (-6, -5,  -6,  -8, -1,  -3,  -5,  -6,  -8,  -10, -12, -13)
        set_rhythm =  (1,   0.5, 0.5, 1,  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1,   1 )
        clef = "bass"
        respell = "sharps"
        metrical_durations = ( ((1,4),)*4 )* 2

class PhraseBlock4(calliope.PhraseBlock):
    
    class Soprano(calliope.Phrase):
        set_pitches = (7, 9,   11,  12, 11, 12,  11,  9, 8, 9)
        set_rhythm =  (1, 0.5, 0.5, 1,  1,  0.5, 0.5, 1, 1, 1)
        respell = "sharps"

    class Alto(calliope.Phrase):
        set_pitches = (-1, -3, 9, 8, 9, 4, 4, 4)
        set_rhythm =  ( 1,  1, 1, 1, 1, 1, 1, 1)
        respell = "sharps"

    class Tenor(calliope.Phrase):
        set_pitches = (4,   2,   0,   2,   4, 4, 4,   2,   0, -1, 0)
        set_rhythm =  (0.5, 0.5, 0.5, 0.5, 1, 1, 0.5, 0.5, 1,  1, 1)
        clef = "bass"
        respell = "sharps"

    class Bass(calliope.Phrase):
        set_pitches = (-8, -7, -12, -10, -8, -15, -13, -12, -10, -8, -15)
        set_rhythm =  ( 1,  1,  0.5, 0.5, 1,  0.5, 0.5, 0.5, 0.5, 1,  1 )
        clef = "bass"
        respell = "sharps"
        metrical_durations = ( ((1,4),)*4 )* 2

class PhraseBlock5(calliope.PhraseBlock):
    
    class Soprano(calliope.Phrase):
        set_pitches = (9, 16, 12, 14, 16, 14, 12, 11)
        set_rhythm =  (1, 1,  1,  1,  1,  1,  1,  1 )

    class Alto(calliope.Phrase):
        set_pitches = (4, 4, 4, 5, 7, 6,   8,   9, 4)
        set_rhythm =  (1, 1, 1, 1, 1, 0.5, 0.5, 1, 1)
        respell = "sharps"

    class Tenor(calliope.Phrase):
        set_pitches = (0, -1, -3, -3, -2, -3,  -8,  -6, -4)
        set_rhythm =  (1,  1,  1,  1,  1,  0.5, 0.5, 1,  1)
        clef = "bass"
        respell = "sharps"

    class Bass(calliope.Phrase):
        set_pitches = (-3, -4, -3,  -5,  -7,  -8,  -10, -11, -10, -9, -8)
        set_rhythm =  ( 1,  1,  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1,   1,  1)
        clef = "bass"
        respell = "sharps"
        metrical_durations = ( ((1,4),)*4 )* 2


c1 = calliope.MatchSequence(
    PhraseBlock1("p1"), 
    PhraseBlock2("p2"),
    PhraseBlock3("p3"),
    PhraseBlock4("p4"), 
    PhraseBlock5("p5"),
    )

c1["p5"]["Tenor"].events[4].respell = "flats"

# why doesn't this work with bass clef??
# for p in c1[0]:
#     p.events.insert(0, calliope.Event(beats=3, pitch=None))

for pb in c1:
    for p in pb:
        p.non_rest_events[-1].tag(">")


repeats = 8
phrases_1_repeats = []
for i in range(repeats):
    p1 = PhraseBlock1("p1_ %s" % i)
    for v in p1:
        v.rhythm = [t/2 for t in v.rhythm[:-1]] + [v.rhythm[-1]]
        v.metrical_durations=(((1,4),)*5)
    phrases_1_repeats.append(p1)
    

c2 = calliope.MatchSequence(*phrases_1_repeats)

# print(p["Soprano"].events.beats)

# p.events(pitch=11)(0,-1).setattrs(pitch=0)
# p["Soprano"].events(pitch__gt=12).tag(">")


# class ChoraleGrid(calliope.LineBlock):


calliope.illustrate_me(bubble=c2.get_inverted())