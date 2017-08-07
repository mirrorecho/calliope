# -*- encoding: utf-8 -*-
import copy, abjad
from calliope import tools, structures, bubbles, machines

# TO DO... re-add TagSet once this is properly implemented
# TO DO... how/whether to use this????
# class LeafData(structures.TagSet, structures.Tree):
# class LeafData(structures.Tree):
#     original_duration = 0
#     ticks = 0
#     rest = False

# TO DO... re-add TagSet once this is properly implemented
# class MachineBubbleBase(structures.TagSet, structures.Tree, bubbles.LineTalea):

class BlockMixin(bubbles.SimulLine):

    def comp(self): #????????
        pass

    @property
    def ticks(self):
        return max([c.ticks for c in self])
        

class Machine(bubbles.Line):

    # TO DO... create a way to automate metrical durations for workshopping/testing
    metrical_durations = ( (1,1),(1,1) ) 
    rhythm_default_multiplier = 8
    rhythm_denominator = 32


    # TO DO... screwy?
    def __call__(self, name=None, **kwargs):
        return_bubble = copy.deepcopy(self)
        if name:
            return_bubble.name = name
        for name, value in kwargs.items():
            setattr(return_bubble, name, value)
        return return_bubble

    def get_metrical_duration_ticks(self):
        """
        returns a number representing the total number of ticks in this line (relative to the object's rhythm_denominator)
        .... based on the defined metrical durations for this object
        """
        return int(sum([d[0]/d[1] for d in self.metrical_durations]) * self.rhythm_denominator)


    def cleanup_data(self, **kwargs):

        # self.info("", self.logical_ties)
        def remove_empty_ancestors(tree_item):
            parent_item = tree_item.parent
            if parent_item and not tree_item.children:
                parent_item.remove(tree_item)
                remove_empty_ancestors(parent_item)

        last_rest = None

        for leaf in self.leaves:
            parent_item = leaf.parent
            if not isinstance(leaf, machines.LogicalTie):
                # just in case there are already empty events / segments showing up as leaves ... remove them
                parent_item.remove(leaf)
            else:
                logical_tie = leaf
                if last_rest is not None and logical_tie.rest:
                    last_rest.ticks += logical_tie.ticks
                    parent_item.remove(logical_tie)
                elif logical_tie.rest:
                    last_rest = logical_tie
                else:
                    last_rest = None 
                # print(logical_tie.graph_order)
                if logical_tie.ticks <= 0:
                    self.warn("0/negative ticks detected and removed...", logical_tie)
                    parent_item.remove(logical_tie)

            # now, remove empty parents and grandparents
            remove_empty_ancestors(parent_item)

    def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_count, **kwargs):
        if not data_logical_tie.rest:
            event = data_logical_tie.parent
            pitch = data_logical_tie.pitch or event.pitch
            # TO DO... consider level at which respell should be defined...
            if  isinstance(pitch, (list, tuple)):
                if event.respell=="flats":
                    named_pitches = [abjad.NamedPitch(p).respell_with_flats() for p in pitch]
                elif event.respell=="sharps":
                    named_pitches = [abjad.NamedPitch(p).respell_with_sharps() for p in pitch]
                else:
                    named_pitches = [abjad.NamedPitch(p) for p in pitch]
                # NOTE, decided to implement here (as opposed to in harmony machine), because want chords to be able to be implemented generally
                for note in music_logical_tie:
                    chord = abjad.Chord()
                    chord.note_heads = named_pitches
                    chord.written_duration = copy.deepcopy(note.written_duration)
                    m = abjad.mutate([note])
                    m.replace(chord)
            elif isinstance(pitch, (int, str)):
                if event.respell=="flats":
                    named_pitch = abjad.NamedPitch(pitch).respell_with_flats()
                elif event.respell=="sharps":
                    named_pitch = abjad.NamedPitch(pitch).respell_with_sharps()
                else:
                    named_pitch = abjad.NamedPitch(pitch)
                for note in music_logical_tie:
                    note.written_pitch = named_pitch
            else:
                self.warn("can't set pitch because '%s' is not str, int, list, or tuple" % pitch,  data_logical_tie )

    def get_talea(self):
        return abjad.rhythmmakertools.Talea(self.get_signed_ticks_list(append_rest=True), self.rhythm_denominator)

    def get_rhythm_maker(self):
        return abjad.rhythmmakertools.TaleaRhythmMaker(
            talea=self.get_talea(),
            read_talea_once_only=True,
            # read_talea_once_only = False, # for testing only...
            # division_masks=division_masks, # for testing only...
            # extra_counts_per_division=extra_counts_per_division, # for testing only...
        )

    def get_rhythm_music(self, **kwargs):
        # return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations.flattened()])
        return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations])

    def process_rhythm_music(self, music, **kwargs):
        self.cleanup_data()
        music_logical_ties = tools.by_logical_tie_group_rests(music)
        leaf_count=0
        for music_logical_tie, data_logical_tie in zip(music_logical_ties, self.logical_ties):
            # print( "TL: %s" % leaf_count  )
            # print(music_logical_tie)
            self.process_logical_tie(music, music_logical_tie, data_logical_tie, leaf_count, **kwargs)
            leaf_count += len(music_logical_tie)

    def music(self, **kwargs):
        my_music = self.container_type( self.get_rhythm_music(**kwargs) )
        self.process_rhythm_music(my_music, **kwargs)
        return my_music

    @property
    def logical_ties(self):
        return self.leaves

    @property
    def beats(self):
        return self.ticks / self.rhythm_default_multiplier

class EventMachine(Machine):
    def __init__(self, *args, **kwargs):
        rhythm = kwargs.pop("rhythm", None)
        pitches = kwargs.pop("pitches", None)

        super().__init__(*args, **kwargs)
        if rhythm:
            self.rhythm = rhythm
        if pitches:
            self.pitches = pitches

    @property
    def ticks(self):
        return sum([l.ticks for l in self.logical_ties])

    @property
    def ticks_before(self):
        if self.children:
            return self.children[0].ticks_before
        return 0

    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks

    @property
    def rhythm(self):
        return [l.beats for l in self.logical_ties]

    def append_rhythm(self, beats):
        # note, this is overriden on Event so that events will create a rhythm out of 
        # logical ties as opposed to events of events in an infinite loop
        self.append( machines.Event(rhythm=(beats,) ))

    @rhythm.setter
    def rhythm(self, values):
        my_length = len(self.logical_ties)
        for i, v in enumerate(values):
            if i < my_length:
                self.logical_ties[i].beats = v
            else:
                self.append_rhythm(v)

    @property
    def pitches(self):
        return self.leaves

    @pitches.setter
    def pitches(self, values):
        my_length = len(self.logical_ties)
        for i, v in enumerate(values[:my_length]):
            if i < my_length:
                self.logical_ties[i].pitch = v
                self.logical_ties[i].rest = v is None

    @property
    def first_non_rest(self):
        for l in self.logical_ties:
            if not l.rest:
                return l

    @property
    def last_non_rest(self):
        for l in self.logical_ties[::-1]:
            if not l.rest:
                return l

    def get_signed_ticks_list(self, append_rest=False):
        # TO DO.. there's probably a more elegant one-liner for this!
        return_list = []
        for l in self.logical_ties:
            return_list.extend(l.get_signed_ticks_list())
        
        if append_rest:
            ticks_end = self.ticks
            metrical_duration_ticks = self.get_metrical_duration_ticks()
            if metrical_duration_ticks > ticks_end:
                return_list.append(int(ticks_end - metrical_duration_ticks))

        return return_list

    def add_bookend_rests(self, beats_before=0, beats_after=0):
        if beats_before > 0:
            first_event = self.logical_ties[0].parent
            first_event.insert(0, machines.LogicalTie(rest=True, beats=beats_before))
        if beats_after > 0:
            last_event = self.logical_ties[-1].parent
            last_event.append(machines.LogicalTie(rest=True, beats=beats_after))

    def remove_bookend_rests(self):
        if self.logical_ties:
            if self.logical_ties[0].rest:
                self.logical_ties[0].parent.pop(0)
        if self.logical_ties:
            if self.logical_ties[-1].rest:
                self.logical_ties[-1].parent.pop(-1)

    # TO DO... add slur
    # def slur()
