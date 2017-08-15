# CALLIOPE DESIGN PRINCIPLES:

# KEEP IT SIMPLE! ... abjad already provides a structure, don't re-invent the wheel

# THINK ABOUT... REPEATABLE VS FLEXIBLE

# - working machines at each level
# - blocks/grids
# - way to get all phrases, cells, events
# - machine arranging
# - machine tagging
# - some creative and convenient ways to construct cells and phrases
# - working sequences
# - auto naming? (or names/attrs optional?)
# - machine querying?
# - test each type of bubble and machine... write auto tests?
# - - - - MORE TESTS FOR APPEND VS [] ON BUBBLES


# cleanup / integration
# - - integrate previous "work" ???
# - - integrate previous "cycles" ???
# - - integrate previous "cloud"
# - - fix sequence weirdness

# ametrical music and systems
# - - boxes and arrows

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

import inspect, abjad
from calliope import tools, bubbles, machines

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

# class Violin1(bubbles.Line):
#     music_contents = "b4 b4"

# class Viola(bubbles.Line):
#     music_contents = "a4 a4"

# c1 = machines.Cell(rhythm=(1, 2, 1.5, 0.5), pitches=("bf", "A4", None, "A4"), 
#     metrical_durations = [(4,4)] * 4,
#     name="c1")

# cb = machines.CellBlock(
#     c1,
#     c1(pitches=(None,"c","c'"), name="c2"),
#     metrical_durations = [(4,4)] * 4,
#     )


class T(machines.Event):

    def tag(self, *args):
        my_ret = Map()
        my_ret.machine = self
        return my_ret


class Map(object):
    """
    """

    machine = None
    index = None

    # TO DO ... implement slice:
    # TO DO ... implement multiple indeces:
    def __getitem__(self, args):
        # self.index = args
        # print("tagging %s with..." % self.index)
        print(args)
        return self

    def __call__(self, *args):
        # print(args)
        return self

    def __str__(self):
        pass

    @property
    def me(self):
        pass

    @property
    def children(self):
        pass

    @property
    def sl(self):
        return self


t = T()

t.tag( ">", "." )

print("-----")

# [9:15]( "." ) should be no problem
# [9:12]("()") would be IDEAL

# class Viola1(FromSomethingr):
#     # fragments = Frag.make(
#     #     Frag.it(2,7, tags="("),
#     #     Frag.it(2,8, tags=")"),
#     #     Frag.it(2,9, tags="-"),
#     #     Frag.it(2,10, tags="-"),
#     #     Frag.it(2,11, tags="("),
#     #     Frag.it(2,12, tags=")"),
#     #     Frag.it(1,10, ),
#     #     Frag.it(1,11, ),
#     #     )
#     arrange_from = SHORT_SCORE.arrange(

#         )


    # TO DO EVENTUALLY, distill fragments down to something like this:
    # bites = Bites(
    #     Off(line=2)[7:10](
    #                     7, tags=["(","<"] )(
    #                     9, duration=3),
    #     Off(line=2)[13](duration=4),
    #     )


class OrAnd(object):
    def __init__(self, *args):
        pass

    def __call__(self, *args):
        # print(args)
        return self

class AndOr(object):
    def __init__(self, *args):
        pass

    def __call__(self, *args):
        # print(args)
        return self


[] <- selector: specifieds nodes to select, and moves selector down one level
() <- call copies selected nodes and returns context to the original level

t(1,2,3,4)


t.copy(
    Map.children()
        [1,2,3,4]()
    )


t.select(
    Map()
    )


t.update(
    Map()
    )

t(
    Map()(
        Map.children()
            [1,3,4]("-", "()"
                Map()
                    [4](".")
            )
        )
    )

class Clarinet1(ArrangeF):
yoyo(
    Map.children() # children, leaves, twigs? (lines/phrases/cells/smallest_cells/events/logical_ties/
        [AndOr(machines.Event)(4), 2, 4:5, 9:10]
        [6][2:46](
            Map()
                [3](".")
                [7]("-")
            )
        [1]( "(" )
        ["line1"][3]( ")", "." )
        [8]( "(" )
        [9:15](
            Map()
                [10](".")
                [11]("-")
            )
        [9:12]("()")
        [12:15].sl
        [16]()
)

class Clarinet1(machines.Line):
    # metrical_durations = MEDIUM_METRICAL_DURATIONS + {
    # 11: ((1,4),(1,4),(2,4),),
    # 19: ((1,4),(1,4),(1,4),(1,4)),
    # 20: ((1,4),(1,4),(2,4)),
    # 24: ((1,4),(1,4),(1,4),(1,4)),
    # 25: ((1,4),(1,4),(2,4)),
    # 26: ((1,4),(1,4),(1,4),(1,4)),
    # 32: ((2,4),(1,4),(1,4),),
    # 35: ((1,4),(1,4),(1,4),(1,4)),
    # }
    phrase1 = SECTION_F.map_phrase( Map.children
        [6][1:9]( Map.me
            [1]("p", "\<")
            [2:4].sl
            [4]("mf", "-", transpose=12)
            [5:7, 7:9, 15:17, 17:19].sl
            )
        )
    phrase2 = SECTION_F.map_phrase( Map.children
        [6][40:49]( Map.me
            [40](".")
            [41:43].sl
            [43,44]("-")
            [45:47].sl
            [47]("-")
            [48](".")
            )
        )
    phrase3 = SECTION_F.map_phrase( Map.children
        [6][55:59, 61:65, 67:73, 78:82]( Map.me
            [55,56]("-")
            [57](".")
            [58, 61, 62]("-")
            [63](".")
            [64,67]("-")
            [68](".")
            [69:71].sl
            [71]("-")
            [72](".")
            [78:80, 80:82].sl
            [81](duration=2.5)
            )
        )
    phrase4 = SECTION_F.map_phrase( Map.children
        [3][58:62,63:71]("-", Map.me
            [58]("\<","mp")
            [61]("f")
            [70](duration=3)
            )
        ))
    phrase5 = SECTION_F.map_phrase( Map.children
        [1][40:58]("-", chord_positions=0, map=Map.children
            [43](duration=2.5)
            [44]("\<")
            [70]("ff",">")
            )
        )


# Q()
#     [6](
#         [1].tag("p","\<"),
#         [2:3].sl(),
#         [5:6].sl(),
#         [7:8].sl(),
#         [15:16].sl(),
#         [17:18].sl(),
#         [40]
#     )


# Q()
#     [6](
#         [1]("p","\<"),
#         [2:3].sl(),
#         [5:6].sl()("fff"), # <- the fff here is st an example
#         [7:8].sl(),
#         [15:16].sl(),
#         [17:18].sl(),
#         [40]("."),
#         [41:42].sl(),
#         [43,44]("_"),
#         [45:46].sl(),
#     )


# WON'T BE POSSIBE WITH SLICES:
# Q()
#     [6](
#         [1]("p","\<"),
#         [2:3].sl,
#         [5:6].sl("fff"), # <- the fff here is st an example
#         [7:8].sl,
#         [15:16].sl,
#         [17:18].sl,
#         [40]("."),
#         [41:42].sl,
#         [43,44]("_"),
#         [45:46].sl,
#     )


# Q()
#     [6](
#         [1]("p","\<"),
#         [2:3].sl,
#         [5:6].sl("fff"), # <- the fff here is st an example
#         [7:8].sl,
#         [15:16].sl,
#         [17:18].sl,
#         [40]("."),
#         [41:42].sl,
#         [43,44]("_"),
#         [45:46].sl,
#     )






# ===========================================================================
# ===========================================================================
# ===========================================================================
# USE THIS!
# ===========================================================================
# ===========================================================================
# ===========================================================================

# class QBase(object):
#     scope = None # "children", "leaves", "nodes", or "self" ... None for not applicable
#     sub_q = None
#     is_filtering_sub_q = False

#     args = None # set to list of: strings (names), ints (indices), slices, types, or methods... which all work similarly for retrieving tree children
#     kwargs = None # set to dictionary to match object attributes

#     def add_arguments(self, *args, **kwargs):
#         for arg in args:
#             if isinstance(arg, QBase):
#                 arg.scope = None # scope has no meaning for sub-logical objects
#                 arg.sub_scope = None
#         #     elif inspect.issubclass(arg, calliope.Bubble):
#         #         self.types.append(arg)
#         #         args.remove(arg)
#         #     elif callable(arg):
#         #         args.methods.append(arg)
#         #         args.remove(arg)
#         self.args.extend(args)
#         self.kwargs.update(kwargs)

#     def __init__(self, *args, **kwargs):
#         self.args = []
#         self.kwargs = {}
#         self.scope = kwargs.pop("scope", None) or self.scope
#         self.add_arguments(*args, **kwargs)
    
#     def last_decendant_q(self):
#         if self.scope_q:
#             return last_decendant_q(self.scope_q)
#         else:
#             return self

#     def __getitem__(self, *args):
#         decendant = self.last_decendant_q()
#         decendant.sub_q = QOr(*args)
#         decendant.sub_q.scope = decendant.sub_scope
#         return self

#     def stringpart(self, line_prefix="    ", line_suffix="\n"):
#         indent = "|  "
#         return_string = ""
#         if self.scope: 
#             return_string += "[" + self.scope + "]" + line_suffix
#         return_string += "%s%s:%s" % (line_prefix, self.logical_name, line_suffix)
#         for arg in self.args:
#             if isinstance(arg, QBase):
#                 return_string += arg.stringpart(line_prefix+indent, line_suffix)
#             else:
#                 return_string += "%s%s%s" % (line_prefix+indent, arg, line_suffix)
#         for key, value in self.kwargs.items():
#             return_string += "%s%s=%s%s" % (line_prefix+indent, key, value, line_suffix)
#         return return_string

#     def __str__(self):
#         return_string = self.stringpart()
#         if self.sub_q:
#             return_string +=  str(self.sub_q) + "\n--------------------------------------"
#         return return_string

#     @property
#     def logical_name(self):
#         if isinstance(self, QOr):
#             return "Or"
#         if isinstance(self, QAnd):
#             return "And"
#         else:
#             return "??"

#     @property
#     def leaves(self):
#         self.scope = "leaves"
#         self.sub_scope = "leaves"
#         return self

#     @property
#     def nodes(self):
#         self.scope = "nodes"
#         self.sub_scope = "nodes"
#         return self

#     @property
#     def children(self):
#         self.scope = "children"
#         self.sub_scope = "children"
#         return self

#     def nodes_in_scope(self, bubble):
#         if self.scope == "self":
#             return (bubble,)
#         if self.scope == "twigs":
#             return [l.parent for l in self.leaves]
#         return getattr(bubble, self.scope, ())

#     def query_nodes(self, bubble):
#         return_nodes = []
#         for i, node in enumerate(self.nodes_in_scope(bubble)):
#             if self.bubble_node_match(node, i):
#                 return_nodes.append(node)
#         return return_nodes

#     def bubble_node_match(self, bubble, index):
#         return True

# class QAnd(QBase):
#     def __call__(self, *args, **kwargs):
#         if len(args) + len(kwargs) > 1:
#             self.add_arguments( QOr(*args, **kwargs) )
#         else:    
#             self.add_arguments(*args, **kwargs)
#         return self

#     def bubble_node_match(self, bubble, index):
#         for arg in self.args:
#             if isinstance(arg, int):
#                 if arg != index:
#                     return False
#             elif isinstance(arg, slice):
#                 print("TO DO...need to implement slice queries!")
#             elif inspect.isinstance(arg, QBase):
#                 if not arg.bubble_node_match(bubble, index):
#                     return False
#             elif isinstance(arg, str):
#                 if bubble.name != arg:
#                     return False
#             elif inspect.isclass(arg):
#                 if not isinstance(bubble, arg):
#                     return False
#             elif callable(arg):
#                 print("TO DO...need to callable queries!")
#         for key, value in kwargs.items():
#             if getattr(bubble, key, None) != value:
#                 return False
#         return True


# class QOr(QBase):
#     def __call__(self, *args, **kwargs):
#         new_and = QAnd(self)
#         new_and.scope = self.scope
#         self.scope = None
#         if len(args) + len(kwargs) > 1:
#             new_and.add_arguments( QOr(*args, **kwargs) )
#         else:    
#             new_and.add_arguments(*args, **kwargs)
#         return new_and

#     def bubble_node_match(self, bubble, index):
#         if not self.args and not self.kwargs:
#             return True
#         for arg in self.args:
#             if isinstance(arg, int):
#                 if arg == index:
#                     return True
#             elif isinstance(arg, slice):
#                 print("TO DO...need to implement slice queries!")
#             elif inspect.isinstance(arg, QBase):
#                 if arg.bubble_node_match(bubble, index):
#                     return True
#             elif isinstance(arg, str):
#                 if bubble.name == arg:
#                     return True
#             elif inspect.isclass(arg):
#                 if isinstance(bubble, arg):
#                     return True
#             elif callable(arg):
#                 print("TO DO...need to callable queries!")
#         for key, value in kwargs.items():
#             if getattr(bubble, key, None) == value:
#                 return True
#         return False

# # class QWith(QBase):
# #     pass

# class QueryMaker(QBase):
#     scope = "self"

#     def __getitem__(self, *args):
#         return_q = QAnd(scope=self.scope)
#         return return_q.__getitem__(*args )


#     def __call__(self, *args, **kwargs):
#         if len(args) + len(kwargs) > 1:
#             return QOr(scope=self.scope, *args, **kwargs)
#         else:    
#             return QAnd(scope=self.scope, *args, **kwargs)


# Q = QueryMaker()

# Q[:] # shorthand for:
# Q.children

# Q.children(a=1, b=2, Q() )

# Q[:-1] # all children except the last
# Q.children[:-1] # same 

# Q(use_me=True)[:-1] # only if root has attr use_me=True, then all children except the last
# Q(use_me=True).children[:-1] # same 

# # vs:
# Q.children(use_me=True)[:-1] # all children that have use_me=True

# Q.children[:-1](use_me=True) # all children that have use_me=True

# Q.children[:-1](use_me=True)[1:]

# # equivalent
# Q.children(1,2,4) # filtered by child index 1,2,4
# Q[1,2,4] # sliced by child index 1,2,4
# Q.children[1,2,4](1,2,4) #sliced by child index 1,2,4; then filtered by child index 1,2,4
# # the above is the same because filtering happens on the original index, not the sliced index

# # but not
# Q.children(1,2,4)[1,2,4].children[:2]
# # this would cause an index error since slicing happens over the filtered results 

# Query()[2]

# G.events[1,2,3,4,5,6,9:60]

#         1,
#         2,
#         6,
#         7,
#         8,
#     ).children(
#         special=True)[1]


# # as an example:
# # USING THESE EVENTS
# 1,2,6,28, 45:60

# b(
#     Q["c1"].with(machines.Phrase)[
#         Q[1],
#         Q[2].with[1].attrs(tags=[">","."], duration=4),
#         Q[5:23].with[:-1],
#     ](myattr1="yes")(myattr2="yes")
#     )
# b.query(
#     Q.children(
#         myattr1="yes", 
#         Q(machines.Cell)(index=1) 
#         )(myattr2="yes")
#     )



# Q.c_[:2](machines.Phrase).n_(machines.LogicalTie)

# q = Q(include_me=True)._[2:5](machines.Line)
# # # returns 3rd, 4th, and fith lines underneath self, only if self has attr include_me=True (otherwise returns empty list)

# q = Q._(fancy=True)._twigs._[0]
# q = Q[:](fancy=True)._twigs._[0]
# # applied to machine, returns the first logical tie of every event that's part of a phrase with attr fancy=True

# q = Q._nodes[:-1](machines.Cell)
# # returns all cells at any level, except the very last cell

# q = Q[:2](machines.Phrase).nodes[:-1](machines.Cell)(long=True)

# q = Q._[:2](machines.Phrase)._nodes[:-1](machines.Cell)(long=True)

# q = Q.logical_ties(pitch_number__gt=14)

# q = Q.smallest_cells(short=False).logical_ties[:2]

# q = Q.events[:24]

# class T:
#     @property
#     def _(self):
#         print("yo")

# t = T()
# t._



# q = Q.c_self.c_children

# q = Q.I._[:2](machines.Phrase)(
#     Q(1).inc
#     )

# q = Q[
#         Q(machines.Phrase)(
#             Q[1:3]
#             )[1:3],
#     ]


# q = Q[1,2,3,4](machines.Line)(
#     1, 
#     2, 
#     3, 
#     Q(4)("yoyo1", "yoyo2"), 
#     tag="special_3", 
#     )


# q = Q().children[]
# print(q)

# class QBubble(calliope.Bubble):

#     def query(self, q):
#         print(q.args)

#     def select(self, *args):
#         print(args)

# and vs or relationships
# sequence or match
# of or with? (i.e. certain cells of certain phrases, or certain phrases along with certain cells underneath)
# by name
# by index
# by sice
# by attr = value
# SILVER STAR:lamba
# GOLD STAR: by where

# b = QBubble()
# b(
#     Q["c1"].with(machines.Phrase)[
#         Q[1],
#         Q[2].with[1].attrs(tags=[">","."], duration=4),
#         Q[5:23].with[:-1],
#     ](myattr1="yes")(myattr2="yes")
#     )
# b.query(
#     Q.children(
#         myattr1="yes", 
#         Q(machines.Cell)(index=1) 
#         )(myattr2="yes")
#     )


# ===========================================================================
# ===========================================================================
# ===========================================================================
# END USE THIS!
# ===========================================================================
# ===========================================================================


# # "and", "children", "leaves", "nodes", or "with"
# q = ("children", (

#         )  
#     )

# (
#     Q.next
# )



# BASE_MUSIC = machines.Score(
#     machines.Line(
#         machines.Cell(rhythm=(1,1,1), pitches=("a'", "a'", None)),
#         name="line1"
#         ),
#     machines.Line(
#         machines.Cell(rhythms)
#         name="line2"
#         )
#     machines.Line(
#         machines.Cell(rhythms)
#         name="line3"
#         )
#     )

# tools.illustrate_me()


# import inspect
# # import abjad
# # c = abjad.scoretools.FixedDurationContainer((2,3), "c1")
# # lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(c)
# # print(format(lilypond_file))
# from calliope import bubbles

# class MyBubble(calliope.Bubble):
#   yo = "BAH"


# b1 = MyBubble()
# b2 = calliope.Bubble()
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


