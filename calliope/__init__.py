# core
from calliope.core.base_mixin import BaseMixin
from calliope.core.illustrate_me import illustrate_me
from calliope.core.rhythm import by_logical_tie_group_rests
# from calliope.core.pitch import respell
from calliope.core.tree import SelectableMixin, Tree
from calliope.core.selection import MachineSelectableMixin, Selection
from calliope.core.tag_set import TagSet

# bubbles
from calliope.bubbles.bubble import Bubble
from calliope.bubbles.fragment import Fragment, SegmentMixin, Segment, MultiFragment, SimulFragment
from calliope.bubbles.fragment_ametric import Ametric, AmetricStart
from calliope.bubbles.staff import (Voice, Staff, RhythmicStaff, 
            StaffGroup, Piano, Harp, StaffWithVoices, InstrumentStaffGroup)
from calliope.bubbles.score import Score, AutoScore
from calliope.bubbles.sequence import MatchSequence

# machines
from calliope.machines.machine import BaseMachine, Machine, EventMachine
# ... note the order, inner to outer, is important...
from calliope.machines.logical_tie import LogicalTie
from calliope.machines.event import Event, RestEvent
from calliope.machines.cell import Cell, ContainerCell, CustomCell #, TupletCell 
from calliope.machines.phrase import Phrase
from calliope.machines.line import Line
from calliope.machines.block import Block, EventBlock, CellBlock, PhraseBlock, LineBlock

# machine factories
from calliope.factories.factory import Factory
from calliope.factories.copy_events import CopyEventsFactory
from calliope.factories.stack_pitches import StackPitches

# machine transforms
from calliope.transforms.transform import Transform
from calliope.transforms.transpose import Transpose, Displace, DisplaceFifths
from calliope.transforms.add_constant_pitch import AddConstantPitch
from calliope.transforms.span_by_type import SpanByType, BracketCells, SlurCells
# from calliope.machines.transforms.filtering import Filter, Remove
# from calliope.machines.transforms.line_stacked import StackedTransform, LineStacked
# from calliope.machines.transforms.make_chords import MakeChords 
# from calliope.machines.transforms.sorting import SortByPitch, SortByDuration 
# from calliope.machines.transforms.tagging import Tagging, Slur, BracketByType, BracketCells
# from calliope.machines.transforms.smart_range import SmartRange
# from calliope.machines.transforms.pitches_through_grid import PitchesThroughGrid

# grids
from calliope.grids.grid_base import GridBase
from calliope.grids.tally_base import TallyBase
from calliope.grids.pitches.pitch_grid import PitchGrid
from calliope.grids.pitches.tally_circle_of_fifths_range import TallyCircleOfFifthsRange
from calliope.grids.pitches.tally_melodic_intervals import TallyMelodicIntervals
from calliope.grids.pitches.tally_parallel_intervals import TallyParallelIntervals
from calliope.grids.pitches.tally_repeated_jumps import TallyRepeatedJumps

# libraries
from calliope.libraries import meters
from calliope.libraries.pitch_sequence import PitchSequence

from calliope.core.startup import startup
startup()