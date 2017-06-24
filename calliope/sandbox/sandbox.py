# CALLIOPE DESIGN PRINCIPLES:

# KEEP IT SIMPLE! ... abjad already provides a structure, don't re-invent the wheel

# THINK ABOUT... REPEATABLE VS FLEXIBLE

# - make sure score (and all bubble wraps) still work
# - get basic ilustration working again
# - MORE TESTS FOR APPEND VS [] ON BUBBLES
# - machine tagging

# ametrical music and systems
# - - boxes and arrows

# cleanup / integration
# - - integrate previous "work"
# - - integrate previous "cycles"
# - - integrate previous "cloud"
# - - fix sequence weirdness

# a few tools to help with routine tasks
# - - integrate/refactor score auto-generation from random bubbles with BubbleScore
# - - better templates for scores and parts

# beuatifully printed music (with some fancy formatting)
# - - fonts
# - - better rehearsal marks (score vs parts)
# - - measure numbering at bottom of large scores
# - - instrument names and cues
# - - add/remove staves (and account for this in parts)

# TO DO / NEXT UP
# - - odd / compound time signatures
# - - double and sashed bar lines
# - - start moving through caesium until it kicks you
# - - CLOUDS
# - - "music from durations" rethought
# - - overall arranging rethought
# - - add lilypond comments where bubbles start in voice music
# - - better ametric spanners with time span text

# MISC
# - - piano centered dynamics (see http://lsr.di.unimi.it/LSR/Item?id=357 ??)
# - - unterminated ties


# ---------------------------- FUTURE:
# AUTOMATIC METRICAL DURATIONS (research abjad)
# studio setup!!! 
#  - - - (mac or linux?)
# - - - (mac keyboard / mouse?)
# - - - lower desk is better for tall monitors
# - I LOATHE GARAGE BAND... need some better way to create playback
# - fix clefs in short scores
# - replace some class-defined stuff with modules / introspection (i.e. should not need to create a class to describe grid bubble lines that are described above)
# - think about data cleanup carefully, and adjust
# - parts need to be WAY WAY WAY simpler to generate!!!!
# - - - should be able to specify a few simple settings in module
# - - - separate PDF and Ly files
# - - - simple declaritve file(s) for how score/parts are organized
# - more readable indices (small font, all in a row)
# measures shojuld be 1-based!!!!!
# - tremolos won't work with tied notes
# - conisistency / plan for what's a class attribute and what's not
# - - - maybe attachment stuff not, pitch/rhythm stuff is?
# - better indices/colors
# - separate stylesheets for working score / short score (vs performance score, parts, etc.)
# - refactor standard stuff into callope
# - use asserts for error handling
# - keep relative durations as negative?
# - bug, first rest in rhythm is removed if rhythm_initial_silence is also 0 (can work around be always using rhythm_initial_silence... but this is screwy)
# - could go CRAZY (in a good way) with fragments, inheritance, etc. ... spend time on this, it could be fruitful
# - go through all to dos!
# IMPLEMENTING INTO CALLIOPE:
# - orchestrate first, then short score
# - machines to be arbitrarily applied at logical_tie, event, segment, or phrase level
# - project startup script
# - consistent naming with data children (e.g. don't use "children" ... should always say "events", etc.)
# - adding and removing staves
# - BOXES BOXES BOXES!!!!
# - sponsor lilypond development
# - move some of the arrangement stuff that's currently in base bubble grids to machines / inherited lines (probably would perform better)
# - initial silence is specific to copper ... make it work in another way (or keep it in the inherited copper classes only)
# - go back through rep... ESPECIALLY elements & tokei orchestra pieces, accomodate, and make them even better!!!!!!!!!!!!!  (listen to recordints too... )
# - short score illustrations should include staff-level attachments such as tempo, clef, etc.
# - fix illustrate_me funkiness added for OSX sublimetext virtual environment support
# - look ingo abjad's IOManager run_lilypond method ... seems like lilypond_path argument unused... submit a fix?
# - better way to specify header (title, composer, footer, etc) without sticking it in the stylesheet
# - Tuples!!!!
# - deal with changing time signatures within a line
# - - - way to specify
# - - - update multimeasure rest generator to accomodate
# smarter metrical durations (notes vs rests vs beaming)
# - be clear about what accepts kwargs and what does not... 
# - better way to show pitch indices in harmony
# - color code lines, and fragments by line (just tag color... that's enough!)
# - smart auto-respell pitches
# - think of sending lines TO fragments in other lines (instead of pulling FROM)?
# - even cleaner fragments, with slicing and pattern-based alterations/tagging (see Viola1 in orchestration_c)
# - - - including patterns on fragments (or frag it/line) added together
# - use inheritance better with fragments
# - tagging to handle trills
# - easily construct phrases/segments/events/logical-ties more manually
# - harmonics machine (reconstitute)
# - tag at the logical tie/leaf level when defining fragments
# - simple method to slur a bunch of notes with following notes 
# - piano/harp/etc. part that can combine events from different lines
# - refactor so that all fragments.update_by should not be necessary
# - better error handling when overlapping events create sorting problems in fragments
# - odd problems if fragments moved before other fragments... fix?
# - smarter tagging with patterns!!! (and based on note duration and jump)
# - smarter dynamics tagging
# - better way to distinguish short score from regular score
# - auto breaths for wind/brass
# - REMEMBER THAT THE END TAKES A LONG TIME
# - for future reference, add more articulations, dymacics BEFORE orchestrating... will save time
# - auto assign clefs
# - - - for short scores
# - - - based on instrument preferences
# - automate start and stop together orchestration (assign stops/starts)
# - smarter pitch displacement (stay within range / range of fifths)
# - cross lines using rhythm overlay (including mixing together into chords)
# - pulse machine that separates pulses into separate events (so that each pitch can be displaced)
# - tag to show any data attribute
# - smarter error handling
# - better tempo management (why does it slow everything down?) 
# - - - - including metric modulation (see http://abjad.mbrsi.org/api/tools/indicatortools/MetricModulation.html)
# - allow slices of data to be tagged
# - better way to handle octave transposing instruments in scores
# - maybe. .. warn if orchestrated lines don't inherit from arrangement base classes (i.e. they should be getting rehearsal marks, etc.)
# - (if necessary) - there's a bug with dupe tie spanners on drones (bug show up if you attempt to print Drone0's music() output)
# - show measure numbers on multimeasure rests
# - limit multimeasure rest length to 8 bars? (see below... could create list of lists to determine measure count)
# - - - - - maybe better... limit to 8 only if greater than 9?
# - - - - - also, would be ideal to be able to specify break points... 
# - easily turn colors on and off
# - add events from multiple lines into a single harmonic event
# - beaming tags
# - remember slur_me !
# should be able to easily add instruction AFTER note
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

import abjad
from calliope import tools, bubbles


class MyScore(bubbles.Score):

    class Strings(bubbles.StaffGroup):
        
        class Violins(bubbles.InstrumentStaffGroup):
            class Violin1(bubbles.Staff):
                instrument=abjad.instrumenttools.Violin(
                    instrument_name="Violin 1", short_instrument_name="vln.1")

            class Violin2(bubbles.Staff):
                instrument=abjad.instrumenttools.Violin(
                    instrument_name="Violin 2", short_instrument_name="vln.2")

        class Viola(bubbles.Staff):
            instrument=abjad.instrumenttools.Viola(
                instrument_name="Viola", short_instrument_name="vla.")

        class Cello(bubbles.Staff):
            instrument=abjad.instrumenttools.Cello(
                instrument_name="Cello", short_instrument_name="vc.")
            clef="bass"

class Violin1(bubbles.Line):
    music_string = "b4 b4"

class Viola(bubbles.Line):
    music_string = "a4 a4"

Cello = Viola(music_string="c'2")

tools.illustrate_me(score_type=MyScore)


# import inspect
# # import abjad
# # c = abjad.scoretools.FixedDurationContainer((2,3), "c1")
# # lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(c)
# # print(format(lilypond_file))
# from calliope import bubbles

# class MyBubble(bubbles.Bubble):
#   yo = "BAH"


# b1 = MyBubble()
# b2 = bubbles.Bubble()
# b1["ta"] = bubbles.Line("c1")

# print(b1["yo"])


# class Boo(object):
#   items = ()

#   @classmethod
#   def class_sequence(cls, *args):
#       # print(inspect.stack()[1][0].f_locals)
#       return list(cls.items) + list(args)

#   def sequence(self, *args):
#       # print(inspect.stack()[1][0].f_locals)
#       return list(self.items) + list(args)


# b = Boo()
# b.items = [1,2,3]
# print(Boo.class_sequence(4,5,6))
# print(b.sequence(4,5,6))


