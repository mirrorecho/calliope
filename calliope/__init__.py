# core
from calliope.core.settings import *
from calliope.core.calliope_base import CalliopeBase
from calliope.core.selectable_mixin import SelectableMixin
from calliope.core.tree import Tree
from calliope.core.selection import Selection, ExcludeSelection
from calliope.core.rhythm import by_logical_tie_group_rests
from calliope.core.pitch import set_pitch
from calliope.core.tag_set import TagSet
from calliope.core.illustrate import illustrate, illustrate_me
from calliope.core.to_snake_case import to_snake_case

from calliope.pitch.scale import Scale

# bubbles
from calliope.bubbles.bubble import Bubble
# from calliope.bubbles.fragment import Fragment, SegmentMixin, Segment, MultiFragment, SimulFragment
# from calliope.bubbles.fragment_ametric import Ametric, AmetricStart
from calliope.bubbles.staff import (Voice, Staff, RhythmicStaff, 
            StaffGroup, Piano, Harp, StaffWithVoices, InstrumentStaffGroup)
from calliope.bubbles.score import Score #, AutoScore
from calliope.bubbles.sequence import MatchSequence

# machines
from calliope.machines.machine import Machine
from calliope.machines.fragment import Fragment
from calliope.machines.fragment_row import FragmentRow
# ... note the order, inner to outer, is important...
from calliope.machines.logical_tie import LogicalTie
from calliope.machines.event import Event
from calliope.machines.cell import Cell #, ContainerCell, CustomCell #, TupletCell 
from calliope.machines.phrase import Phrase
from calliope.machines.line import Line
from calliope.machines.segment import Segment
from calliope.machines.fragment_block import FragmentBlock, EventBlock, CellBlock, PhraseBlock, LineBlock, SegmentBlock

Score.startup_root()

# grids
from calliope.grids.grid_base import GridBase
from calliope.grids.tally_base import TallyBase
from calliope.grids.pitches.pitch_grid import PitchGrid
from calliope.grids.pitches.tally_circle_of_fifths_range import TallyCircleOfFifthsRange
from calliope.grids.pitches.tally_melodic_intervals import TallyMelodicIntervals
from calliope.grids.pitches.tally_parallel_intervals import TallyParallelIntervals
from calliope.grids.pitches.tally_repeated_jumps import TallyRepeatedJumps

# machine transforms
from calliope.transforms.transform import Transform
from calliope.transforms.transpose import Transpose, Displace, DisplaceFifths, TransposeWithinScale
from calliope.transforms.add_constant_pitch import AddConstantPitch
from calliope.transforms.span_by_type import SpanByType, BracketCells, SlurCells, PhrasePhrases
from calliope.transforms.stack_pitches import StackPitches
from calliope.transforms.smart_range import SmartRange
from calliope.transforms.crop_chords import CropChords
from calliope.transforms.pulse_events import PulseEvents
from calliope.transforms.poke import Poke
from calliope.transforms.label import Label
from calliope.transforms.overlay import Overlay
from calliope.transforms.scale_rhythm import ScaleRhythm
from calliope.transforms.tenu_stacca import TenuStacca
from calliope.transforms.tag_notes import TagNotes

# from calliope.machines.transforms.filtering import Filter, Remove
# from calliope.machines.transforms.line_stacked import StackedTransform, LineStacked
# from calliope.machines.transforms.make_chords import MakeChords 
# from calliope.machines.transforms.sorting import SortByPitch, SortByDuration 
# from calliope.machines.transforms.tagging import Tagging, Slur, BracketByType, BracketCells
# from calliope.machines.transforms.pitches_through_grid import PitchesThroughGrid

# machine factories
from calliope.factories.factory import Factory, FromSelectableFactory, EventBranchFactory
from calliope.factories.chords_from_selectable import ChordsFromSelectable
from calliope.factories.copy_events import CopyEventsFactory
# from calliope.factories.stack_pitches import StackPitches # TO DO: this is a dupe
from calliope.factories.composite_row import CompositeRow, CompositeCell, CompositeLine, SplayRow
from calliope.factories.pitches_through_grid import PitchesThroughGrid

# libraries
from calliope.libraries import meters
from calliope.libraries.pitch_sequence import PitchSequence

# TO DO... ?
SELECTION_COUNTER = 0

