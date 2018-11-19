# -*- encoding: utf-8 -*-
import math, copy, abjad
from abjadext import rmakers
from abjad import rhythmtrees
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
class BaseMachine(calliope.MachineSelectableMixin, calliope.TagSet):
    create_container = False 
    use_child_metrical_durations = False
    metrical_durations = None
    meter = None
    rhythm_default_multiplier = 8 # TO DO: confusing... think of ticks per beat... instead...
    rhythm_denominator = 32
    set_name = None
    defined_length = None # pre-determined length in beats, will pad rests at end if needed
    can_have_children = True
    must_have_children = True # TO DO: used?
    transforms = () # can be set to any iterable
    factory = None
    is_simultaneous = False
    time_signature = None
    pickup = None # must be able to be represented as a single note with no dots
    clef = None
    bar_line = None
    respell = None # set to "sharps" or "flats"  to force respelling

    # TO DO ... implement default meter here...

    def __init__(self, *args, **kwargs):
        # base class Fragment takes first argument to be music content, if
        # first argment a string... overridden here to represent name of machine instead.
        if len(args) > 0 and type(args[0]) is str:
            self.set_name = args[0]
            args = args[1:]

        if isinstance(self, calliope.Factory):
            self.factory = self
        
        super().__init__(*args, **kwargs)
        
        if self.set_name:
            self.name = self.set_name


        for transform in self.get_transforms():
            transform(self)

    def set_children_from_class(self, *args, **kwargs):
        if self.factory is not None:
            self.factory.fabricate(self, *args, **kwargs) # TO DO... remove args/kwargs here?
        else:
            super().set_children_from_class(*args, **kwargs)

    def get_transforms(self, *args, **kwargs):
        my_transforms = []
        for transform_class_name in type(self).class_sequence( child_types=(calliope.Transform,) ): 
            my_transforms.append( getattr(self, transform_class_name)() )
        my_transforms.extend(self.transforms)
        return my_transforms
                                                            
    # TO DO... apply this same idea more generally for fragments in side of 
    # blocks for things like time_signature
    # TO DO... CONSIDER AS TAG INSTEAD?
    def get_respell(self):
        if self.respell:
            return self.respell
        elif self.parent and isinstance(self.parent, BaseMachine):
            return self.parent.get_respell()


    def process_music(self, music, **kwargs):
        super().process_music(music, **kwargs)

        if len(music) > 0:
            music_start = abjad.select(music).leaves()[0]

            # if self.respell:
            #     calliope.respell(music, self.respell)

            if self.time_signature:
                # TO DO... is the numeric comm*ad necessary... maybe just include it at the score level?
                time_command_numeric =  abjad.LilyPondLiteral(r"\numericTimeSignature", "before")
                abjad.attach(time_command_numeric, music_start)

                time_command =  abjad.LilyPondLiteral(r"\time " + str(self.time_signature[0]) + "/" + str(self.time_signature[1]), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(time_command, music_start)

            if self.pickup:
                partial_value = int((1 / self.pickup) * self.rhythm_denominator / self.rhythm_default_multiplier)
                partial_command =  abjad.LilyPondLiteral(r"\partial " + str(partial_value), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(partial_command, music_start)

            if self.clef:
                clef_obj = abjad.Clef(self.clef)
                abjad.attach(clef_obj, music_start)

            if self.bar_line:
                bar_command =  abjad.LilyPondLiteral(r'\bar "' + self.bar_line + '"', 'before')
                abjad.attach(bar_command, music_start)

class Machine(BaseMachine):

    # TO DO... AUTO MAKE THIS NOT HAVE TO BE 4/4... also, nested for measures/beaming??
    def get_metrical_durations(self):

        if self.metrical_durations:
            return self.metrical_durations
        
        durations = []

        if self.use_child_metrical_durations:
            # TO DO... need to test this! (and probably could be a 1-liner)
            for c in self:
                my_durations.extend(c.get_metrical_durations())
            return durations
        else:
            meter = self.meter or calliope.meters.METER_4_4

            def node_ticks(node):
                return (node.duration.numerator / node.duration.denominator) * self.rhythm_denominator

            def next_sibling_or_aunt(node):
                rel_node = node.root
                if not rel_node:
                    # iff node is already root, than node.root is None
                    # so just return node
                    return node

                rel_node_sib = None
                graph_order = node.graph_order
                ancestor_index = -1
                while node.parent is not None:
                    node = node.parent
                    sibling_index = graph_order[ancestor_index] + 1
                    if len(node) > sibling_index:
                        rel_node = node[sibling_index]
                        rel_node_sib = node[sibling_index]
                        break
                    ancestor_index -= 1
                return rel_node

            # TO DO CONSIDER... use a single instance of abjad.Meter in meters library?
            current_node = abjad.Meter(meter).root_node
            
            if self.pickup:
                # if there's a pickup, try to match metrical node with the pickup...
                pickup_pair = (1, int((1 / self.pickup) * self.rhythm_denominator / self.rhythm_default_multiplier))
                current_node = next((n for n in reversed(current_node.nodes) if n.duration.pair == pickup_pair), current_node)

            meter_ticker = 0
            logical_tie_ticker = 0

            """ LOGIC BELOW IS:
            - REPEAT WHILE CURRENT NODE STARTS BEFORE END OF LT
                - while current node ends after lt and able to sub-divide, then sub-divide
                - add current node
                - current node moves to next sibling or next aunt or root
            - MOVE TO NEXT LT
            """

            for ticks in self.get_signed_ticks_list():

                while meter_ticker < logical_tie_ticker + abs(ticks):

                    while meter_ticker + node_ticks(current_node) > logical_tie_ticker + abs(ticks) \
                            and isinstance(current_node, rhythmtrees.RhythmTreeContainer):
                        current_node = current_node[0]

                    durations.append(current_node.duration.pair)
                    meter_ticker += node_ticks(current_node)               
                    current_node = next_sibling_or_aunt(current_node)

                logical_tie_ticker += abs(ticks) # abs necessary?

        # self.info(durations)
        return durations

    def cleanup_data(self, **kwargs):

        # self.info("", self.logical_ties)
        def remove_empty_ancestors(tree_item):
            parent_item = tree_item.parent
            if parent_item and not tree_item.children:
                parent_item.remove(tree_item)
                remove_empty_ancestors(parent_item)

        last_rest = None

        # removes empty nodes if the nodes are types that should have children
        # and merges sequentual rests
        # TO DO: consider... only merge rests if not tagged?
        for logical_tie in self.logical_ties:
            parent_item = logical_tie.parent
            if logical_tie.must_have_children:
                # TO DO... keep this? Necessary?
                parent_item.remove(logical_tie)
            else:
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

            # now, remove empty parents ands grandparents
            remove_empty_ancestors(parent_item)

    def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_index, **kwargs):
        # data_logical_tie.info(data_logical_tie.parent.name)

        # TO DO... THIS IS NOT THE BEST PLACE FOR THIS LOGIC... REFACTOR
        # TO DO... cast as float
        def get_pitch_number(pitch_thingy):
            if isinstance(pitch_thingy, int):
                return pitch_thingy
            else:
                return abjad.NamedPitch(pitch_thingy).number

        if isinstance(data_logical_tie, calliope.ContainerCell):
            custom_music = data_logical_tie.music()
            m = abjad.mutate(music_logical_tie)
            m.replace(custom_music)

        elif not data_logical_tie.rest:

            event = data_logical_tie.parent
            pitch = data_logical_tie.pitch
            if pitch is None: # note, have to test specifically for None, since 0 has measning here!
                pitch = event.pitch
            respell = data_logical_tie.get_respell()


            # TO DO: code below is clunky... refactor
            if isinstance(pitch, (list, tuple)):
                if respell=="flats":
                    named_pitches = [abjad.NamedPitch(get_pitch_number(p))._respell_with_flats() for p in pitch]
                elif respell=="sharps":
                    named_pitches = [abjad.NamedPitch(get_pitch_number(p))._respell_with_sharps() for p in pitch]
                else:
                    named_pitches = [abjad.NamedPitch(get_pitch_number(p)) for p in pitch]
                # NOTE, decided to implement here (as opposed to in harmony machine), because want chords to be able to be implemented generally
                for note in music_logical_tie:
                    chord = abjad.Chord()
                    chord.note_heads = named_pitches
                    chord.written_duration = copy.deepcopy(note.written_duration)
                    m = abjad.mutate([note])
                    m.replace(chord)
            elif isinstance(pitch, (int, str, abjad.Pitch)):
                # print("MEOW")
                # TO DO: these respell methods look to be private///
                # invetigate further or change!!!!!
                # ALSO TO DO... BUG WITH cf or bs OCTAVES! (workaround is to always convert to # first)
                if respell=="flats":
                    named_pitch = abjad.NamedPitch(get_pitch_number(pitch))._respell_with_flats()
                elif respell=="sharps":
                    named_pitch = abjad.NamedPitch(get_pitch_number(pitch))._respell_with_sharps()
                else:
                    named_pitch = abjad.NamedPitch(get_pitch_number(pitch))
                for note in music_logical_tie:
                    note.written_pitch = named_pitch
            else:
                self.warn("can't set pitch because '%s' is not abjad.Pitch, str, int, list, or tuple" % pitch,  data_logical_tie )

        # TO DO: these loops could be cleaner...
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
                        # used for coloring, maybe other stuff in the future
                        # TO DO: may not be working correctly... need to set up test
                        stop_index = music_leaf_index + len(music_logical_tie)
                        attachment(music[music_leaf_index:stop_index])
                    else:
                        # stem tremolos should be attached to every leaf in logical tie...
                        if isinstance(attachment, abjad.StemTremolo):
                            stop_index = music_leaf_index + len(music_logical_tie)
                            for leaf in music[music_leaf_index:stop_index]:
                                abjad.attach(attachment, leaf)
                        else:
                            abjad.attach(attachment, music[music_leaf_index])


    def get_rhythm_music(self, **kwargs):
        self.cleanup_data()

        ticks_list = self.get_signed_ticks_list()
        my_ticks = sum([abs(t) for t in ticks_list])

        metrical_durations = self.get_metrical_durations()
        metrical_durations_ticks = int(sum([ (d[0]/d[1]) * self.rhythm_denominator for d in metrical_durations]))

        # add rest at end if needed to prevent talea problems if metrical durations
        # length is greater than music (my_ticks) length
        if my_ticks < metrical_durations_ticks:
            ticks_list.append(my_ticks-metrical_durations_ticks)

        talea = rmakers.Talea(
            counts=ticks_list, 
            denominator=self.rhythm_denominator)
        talea_rmaker = rmakers.TaleaRhythmMaker(
            talea=talea,
            read_talea_once_only=True,
            beam_specifier=rmakers.BeamSpecifier(
                beam_each_division=True,
                beam_rests=True,
                ),
            # read_talea_once_only = False, # for testing only...
            # division_masks=division_masks, # for testing only...
            # extra_counts_per_division=extra_counts_per_division, # for testing only...
        )

        leaf_selections = talea_rmaker([abjad.Duration(d) for d in self.get_metrical_durations()])
        return self.container_type(components=leaf_selections, **kwargs)

    def process_rhythm_music(self, music, **kwargs):
        self._open_spanners = {} # important in case music() metchod gets called twice on the same object
        music_logical_ties = calliope.by_logical_tie_group_rests(music)
        leaf_count=0
        # for music_logical_tie, data_logical_tie in zip(music_logical_ties, self.logical_ties_or_container):
        # TO DO: consider check for unequal length of musical_logical_ties/self.logical_ties_or_container?
        # e.g. look at abjad.Sequence        
        pairs = zip(music_logical_ties, self.logical_ties_or_container)

        # raise Exception(list(pairs))
        for music_logical_tie, data_logical_tie in pairs:
            # raise(data_logical_tie)
            # print( "TL: %s" % leaf_count)
            #print(music_logical_tie)
            self.process_logical_tie(music, music_logical_tie, data_logical_tie, leaf_count, **kwargs)
            leaf_count += len(music_logical_tie)

    def music(self, **kwargs):
        my_music = self.get_rhythm_music(**kwargs)
        self.process_rhythm_music(music=my_music, **kwargs)
        return my_music

    @property
    def beats(self):
        return self.ticks / self.rhythm_default_multiplier


