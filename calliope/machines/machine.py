# -*- encoding: utf-8 -*-
import math, copy, abjad
import calliope

# TO DO... re-add TagSet once this is properly implemented
# TO DO... how/whether to use this????
# class LeafData(calliope.TagSet, calliope.Tree):
# class LeafData(calliope.Tree):
#     original_duration = 0
#     ticks = 0
#     rest = False

# TO DO... re-add TagSet once this is properly implemented
# class MachineBubbleBase(calliope.TagSet, calliope.Tree, bubbles.LineTalea):
class BaseMachine(calliope.TagSet):
    # TO DO... create a way to automate metrical durations for workshopping/testing
    metrical_durations = None
    rhythm_default_multiplier = 8
    rhythm_denominator = 32
    # TO DO ... implement default meter here...

    def __init__(self, *args, **kwargs):
        self.transforms_tree = calliope.Transform()
        for transform_name in type(self).class_sequence( child_types=(calliope.Transform,) ): 
            transform_node = getattr(self, transform_name)
            self.transforms_tree[transform_name] = transform_node
        
        self.transforms_tree._transform_setup(self)
        super().__init__(*args, **kwargs)

        # NOTE: since Machine overrides the process_music method,
        # these are implemented here as tags for consinstency with base Fragment method
        if self.time_signature:
            self.tag("\\numericTimeSignature")
            self.tag("time " + str(self.time_signature[0]) + "/" + str(self.time_signature[1]))
        if self.clef:
            self.tag(self.clef)
        if self.bar_line:
            self.tag(self.bar_line)

        self.transforms_tree._transform_nodes(self)

    @property
    def events(self):
        return self.by_type(calliope.Event)

    @property
    def non_rest_events(self):
        return [e for e in self.events if not e.rest]

    @property
    def cells(self):
        return self.by_type(calliope.Cell)

    @property
    def phrases(self):
        return self.by_type(calliope.Phrase)

    @property
    def logical_ties(self):
        return self.leaves # TO CONSIDER: better to select leaves or select by type=LogicalTie???

class Block(BaseMachine, calliope.SimulFragment):

    def comp(self): #????????
        pass

    @property
    def ticks(self):
        return max([c.ticks for c in self])


class Machine(BaseMachine, calliope.Fragment):

    # TO DO... AUTO MAKE THIS NOT HAVE TO BE 4/4... also, nested for measures/beaming??
    def get_metrical_durations(self):
        return self.metrical_durations or ( (4,4), ) * math.ceil(self.beats / 4)

    def get_metrical_duration_ticks(self):
        """
        returns a number representing the total number of ticks in this line (relative to the object's rhythm_denominator)
        .... based on the defined metrical durations for this object
        """
        return int(sum([d[0]/d[1] for d in self.get_metrical_durations()]) * self.rhythm_denominator)

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
            if not isinstance(leaf, calliope.LogicalTie):
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

    def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_index, **kwargs):
        # data_logical_tie.info(data_logical_tie.parent.name)
        if not data_logical_tie.rest:
            # TO DO: consider... can rests be taged????

            event = data_logical_tie.parent
            pitch = data_logical_tie.pitch
            if pitch is None: # note, have to test specifically for None, since 0 has measning here!
                pitch = event.pitch
            respell = data_logical_tie.get_respell()
            
            # TO DO: code below is clunky... refacto
            if isinstance(pitch, (list, tuple)):
                if respell=="flats":
                    named_pitches = [abjad.NamedPitch(p).respell_with_flats() for p in pitch]
                elif respell=="sharps":
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
            elif isinstance(pitch, (int, str, abjad.Pitch)):
                if respell=="flats":
                    named_pitch = abjad.NamedPitch(pitch).respell_with_flats()
                elif respell=="sharps":
                    named_pitch = abjad.NamedPitch(pitch).respell_with_sharps()
                else:
                    named_pitch = abjad.NamedPitch(pitch)
                for note in music_logical_tie:
                    note.written_pitch = named_pitch
            else:
                self.warn("can't set pitch because '%s' is not abjad.Pitch, str, int, list, or tuple" % pitch,  data_logical_tie )

            for tag_name in data_logical_tie.get_all_tags():
                spanners_to_close = set(self._open_spanners) & calliope.TagSet.spanner_closures.get(tag_name, set() )
                for p in spanners_to_close:
                    spanner = data_logical_tie.get_attachment(p)
                    start_index = self._open_spanners[p]
                    stop_index = music_leaf_index + 1
                    if isinstance(spanner, abjad.Slur):
                        # slurs go to the end of the logical tie, not the beginning
                        stop_index += len(music_logical_tie) - 1
                    abjad.attach(spanner, music[start_index:stop_index])
                    del self._open_spanners[p]

            # NOTE... here it's important to through attachments a second time... or we might delete the attachment we just added!! (and get an 
            # eratic exception that's confusing since it would depend on the arbitrary order of looping through the set)
            for tag_name in data_logical_tie.get_all_tags():            
                if tag_name in calliope.TagSet.start_spanners_inventory:
                    self._open_spanners[tag_name]=music_leaf_index
                else:
                    attachment = data_logical_tie.get_attachment(tag_name)
                    if attachment:
                        if callable(attachment):
                            # TO DO... this won't work with chords!
                            # attachment(music_logical_tie)
                            stop_index = music_leaf_index + len(music_logical_tie)
                            attachment(music[music_leaf_index:stop_index])
                        else:
                            # stem tremolos should be attached to every leaf in logical tie...
                            if isinstance(attachment, abjad.indicatortools.StemTremolo):
                                stop_index = music_leaf_index + len(music_logical_tie)
                                for leaf in music[music_leaf_index:stop_index]:
                                    abjad.attach(attachment, leaf)
                            else:
                                abjad.attach(attachment, music[music_leaf_index])


    def get_talea(self):
        return abjad.rhythmmakertools.Talea(self.get_signed_ticks_list(append_rest=True), self.rhythm_denominator)

    def get_rhythm_maker(self):
        return abjad.rhythmmakertools.TaleaRhythmMaker(
            talea=self.get_talea(),
            read_talea_once_only=True,
            beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                beam_each_division=True,
                beam_rests=True,
                ),
            # read_talea_once_only = False, # for testing only...
            # division_masks=division_masks, # for testing only...
            # extra_counts_per_division=extra_counts_per_division, # for testing only...
        )

    def get_rhythm_music(self, **kwargs):
        # return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations.flattened()])
        return self.get_rhythm_maker()([abjad.Duration(d) for d in self.get_metrical_durations()])

    def process_rhythm_music(self, music, **kwargs):
        self.cleanup_data()
        self._open_spanners = {} # important in case music() metchod gets called twice on the same object
        music_logical_ties = calliope.by_logical_tie_group_rests(music)
        leaf_count=0
        for music_logical_tie, data_logical_tie in zip(music_logical_ties, self.logical_ties):
            # print( "TL: %s" % leaf_count  )
            # print(music_logical_tie)
            self.process_logical_tie(music, music_logical_tie, data_logical_tie, leaf_count, **kwargs)
            leaf_count += len(music_logical_tie)

    def process_music(self, music, **kwargs):
        # NOTE: intentionally NOT calling super().process_music here
        # because Fragment's process_music method would conflict...
        pass

    def music(self, **kwargs):
        my_music = self.container_type( self.get_rhythm_music(**kwargs) )
        self.process_rhythm_music(my_music, **kwargs)
        return my_music

    @property
    def beats(self):
        return self.ticks / self.rhythm_default_multiplier

class EventMachine(Machine):
    bookend_rests = ()
    get_children = None
    set_rhythm = None

    # TO CONSIDER... SEPARATE ABOVE EVENT FROM EVENT ITSELF

    def __init__(self, *args, **kwargs):
        rhythm = kwargs.pop("rhythm", None) or self.set_rhythm
        pitches = kwargs.pop("pitches", None)
        pitches_skip_rests = kwargs.pop("pitches_skip_rests", False)
        super().__init__(*args, **kwargs)

        if self.get_children:
            self.extend( self.get_children() )

        if rhythm:
            self.rhythm = rhythm

        if pitches:
            if pitches_skip_rests:
                pitches = list(pitches)
                for i,e in enumerate(self.events):
                    if e.rest and i <= len(pitches):
                        pitches.insert(i, None)
            self.pitches = pitches

        if self.bookend_rests:
            self.add_bookend_rests(*self.bookend_rests)

    @property
    def ticks(self):
        return sum([l.ticks for l in self.logical_ties])

    @property
    def rest(self):
        return all([l.rest for l in self.logical_ties])

    @rest.setter
    def rest(self, is_rest):
        for l in self.logical_ties:
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!

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
        return [l.signed_beats for l in self.logical_ties]

    def append_rhythm(self, beats):
        # note, this is overriden on Event so that events will create a rhythm out of 
        # logical ties as opposed to events of events in an infinite loop
        self.append( calliope.Event(rhythm=(beats,) ))

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
        return (l.pitch for l in self.events)

    @property
    def logical_tie_pitches(self):
        return (l.pitch for l in self.logical_ties)

    @pitches.setter
    def pitches(self, values):
        my_length = len(self.events)
        for i, v in enumerate(values[:my_length]):
            self.events[i].pitch = v
            self.events[i].rest = v is None

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


    def transpose(self, interval):
        for thing in self.by_type(calliope.Event, calliope.LogicalTie):
            # TO DO... handle tuples
            if thing.pitch is not None:
                if isinstance( thing.pitch, (list, tuple) ):
                    for i, pitch in thing.pitch:
                        thing.pitch[i] = abjad.NamedPitch(thing.pitch[i]).transpose(interval)
                else:
                    thing.pitch = abjad.NamedPitch(thing.pitch).transpose(interval)

    def add_bookend_rests(self, beats_before=0, beats_after=0):
        if beats_before > 0:
            first_event = self.logical_ties[0].parent
            first_event.insert(0, calliope.LogicalTie(rest=True, beats=beats_before))
        if beats_after > 0:
            # print(self.logical_ties)
            last_event = self.logical_ties[-1].parent
            last_event.append(calliope.LogicalTie(rest=True, beats=beats_after))

    # TO DO: consider making this cyclic???
    def remove_bookend_rests(self):
        if self.logical_ties:
            if self.logical_ties[0].rest:
                self.logical_ties[0].parent.pop(0)
        if self.logical_ties:
            if self.logical_ties[-1].rest:
                self.logical_ties[-1].parent.pop(-1)

    # TO DO... add slur
    # def slur()
