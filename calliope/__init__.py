# tools
from calliope.tools.basic import illustrate_me
from calliope.tools.rhythm import by_logical_tie_group_rests
from calliope.tools.pitch import respell

# structures
from calliope.structures.tree import TreeMixin, Tree
from calliope.structures.tag_set import TagSet

# bubbles
from calliope.bubbles.bubble import Bubble
from calliope.bubbles.fragment import Fragment, SegmentMixin, Segment, MultiFragment, SimulFragment
from calliope.bubbles.fragment_ametric import Ametric, AmetricStart
from calliope.bubbles.staff import (Voice, Staff, RhythmicStaff, CopyChildrenBubble, 
            StaffGroup, Piano, Harp, StaffWithVoices, InstrumentStaffGroup)
from calliope.bubbles.score import Score, AutoScore
from calliope.bubbles.sequence import MatchSequence

# machines
from calliope.machines.machine import BaseMachine, Block, Machine, EventMachine
# ... note the order, inner to outer, is important...
from calliope.machines.logical_tie import LogicalTie
from calliope.machines.event import Event, RestEvent
from calliope.machines.cell import Cell #, TupletCell, CellBlock 
from calliope.machines.phrase import Phrase #, PhraseBlock
from calliope.machines.line import Line, LineBlock

# machine transforms
from calliope.machines.transforms.transform import Transform
from calliope.machines.transforms.filtering import Filter, Remove
from calliope.machines.transforms.line_stacked import StackedTransform, LineStacked
from calliope.machines.transforms.make_chords import MakeChords 
from calliope.machines.transforms.sorting import SortByPitch, SortByDuration 
from calliope.machines.transforms.tagging import Tagging, Slur
from calliope.machines.transforms.transpose import Transpose, Displace, DisplaceFifths

# clouds
from calliope.cloud.pitches import (TallyAppBase, TallyRepeatedJumps, TallyMelodicIntervals,
    TallyParallelIntervals, TallyCircleOfFifthsRange, CloudPitches)
