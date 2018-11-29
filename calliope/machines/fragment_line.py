import abjad
import calliope

class FragmentLine(calliope.Fragment):
    is_simultaneous = False
    metrical_durations = None
    use_child_metrical_durations = False

    @property
    def ticks(self):
        return sum([l.ticks for l in self.logical_ties])

    def get_signed_ticks_list(self):
        # TO DO.. there's probably a more elegant one-liner for this!
        return_list = [t.signed_ticks for t in self.logical_ties]
        
        if self.defined_length:
            ticks_end = self.ticks
            defined_length_ticks = self.defined_length * calliope.MACHINE_TICKS_PER_BEAT
            if defined_length_ticks > ticks_end:
                return_list.append(int(ticks_end - defined_length_ticks))

        return return_list


    # TO DO ... implement default meter here...
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
                return (node.duration.numerator / node.duration.denominator) * calliope.MACHINE_TICKS_PER_WHOLE

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
                pickup_pair = (1, int((1 / self.pickup) * calliope.MACHINE_BEATS_PER_WHOLE))
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
        for node in self.nodes:
            parent_item = node.parent

            if parent_item and node.must_have_children and len(node)==0:
                parent_item.remove(node)

            elif isinstance(node, calliope.LogicalTie):
                if last_rest is not None and node.rest:
                    last_rest.ticks += node.ticks
                    parent_item.remove(logical_tie)
                elif node.rest:
                    last_rest = node
                else:
                    last_rest = None 
                # print(logical_tie.graph_order)
                if node.ticks <= 0:
                    self.warn("0/negative ticks detected and removed...", node)
                    parent_item.remove(node)

            # now, remove empty parents ands grandparents
            remove_empty_ancestors(parent_item)

    def get_signed_ticks_list(self):
        """ inherited classes should override """ 
        return []


    def get_rhythm_music(self, **kwargs):
        self.cleanup_data()

        ticks_list = self.get_signed_ticks_list()
        my_ticks = sum([abs(t) for t in ticks_list])

        metrical_durations = self.get_metrical_durations()
        metrical_durations_ticks = int(sum([ (d[0]/d[1]) * calliope.MACHINE_TICKS_PER_WHOLE for d in metrical_durations]))

        # add rest at end if needed to prevent talea problems if metrical durations
        # length is greater than music (my_ticks) length
        if my_ticks < metrical_durations_ticks:
            ticks_list.append(my_ticks-metrical_durations_ticks)

        talea = rmakers.Talea(
            counts=ticks_list, 
            denominator=calliope.MACHINE_TICKS_PER_WHOLE)
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

        open_spanners = {}
        music_logical_ties = calliope.by_logical_tie_group_rests(music)
        leaf_count=0

        # TO DO: consider check for unequal length of musical_logical_ties/self.logical_ties_or_container?
        # e.g. look at abjad.Sequence        
        pairs = zip(music_logical_ties, self.logical_ties_or_container)

        for music_logical_tie, data_logical_tie in pairs:

            # TO DO... implement custom cells... maybe like this
            # if isinstance(data_logical_tie, calliope.ContainerCell):
            #     custom_music = data_logical_tie.music()
            #     m = abjad.mutate(music_logical_tie)
            #     m.replace(custom_music)

            if not data_logical_tie.rest:

                my_pitch = data_logical_tie.pitch or event.pitch
                my_respell = data_logical_tie.get_respell()
                calliope.pitch.set_pitch(music_logical_tie, my_pitch, my_respell)


            # TO DO: these loops could be cleaner...
            for tag_name in data_logical_tie.get_all_tags():
                spanners_to_close = set(open_spanners) & calliope.TagSet.spanner_closures.get(tag_name, set() )
                for p in spanners_to_close:
                    spanner = data_logical_tie.get_attachment(p)
                    start_index = open_spanners[p]
                    stop_index = music_leaf_index + 1
                    if isinstance(spanner, abjad.Slur):
                        # slurs go to the end of the logical tie, not the beginning
                        stop_index += len(music_logical_tie) - 1
                    abjad.attach(spanner, music[start_index:stop_index])
                    del open_spanners[p]

            # NOTE... it's important to loop through attachments a second time... or we might delete the attachment we just added!! (and get an 
            # eratic exception that's confusing since it would depend on the arbitrary order of looping through the set)
            for tag_name in data_logical_tie.get_all_tags():
                if tag_name in calliope.TagSet.start_spanners_inventory:
                    open_spanners[tag_name]=music_leaf_index
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

            leaf_count += len(music_logical_tie)

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
                partial_value = int((1 / self.pickup) * calliope.MACHINE_BEATS_PER_WHOLE)
                partial_command =  abjad.LilyPondLiteral(r"\partial " + str(partial_value), "before")
                # TO DO MAYBE: below is cleaner... but abjad only attaches time signature properly to staff (not notes in a container)... workaround?
                # time_command = abjad.TimeSignature( self.time_signature )
                abjad.attach(partial_command, music_start)

            if self.bar_line:
                bar_command =  abjad.LilyPondLiteral(r'\bar "' + self.bar_line + '"', 'before')
                abjad.attach(bar_command, music_start)

    def music(self, **kwargs):
        my_music = self.get_rhythm_music(**kwargs)
        self.process_rhythm_music(music=my_music, **kwargs)
        return my_music

    def add_bookend_rests(self, beats_before=0, beats_after=0):
        if beats_before > 0:
            first_event = self.logical_ties[0].parent
            first_event.insert(0, calliope.LogicalTie(rest=True, beats=beats_before))
        if beats_after > 0:
            last_event = self.logical_ties[-1].parent
            last_event.append(calliope.LogicalTie(rest=True, beats=beats_after))

    # TO DO: consider making this cyclic???
    def remove_bookend_rests(self):
        if self.logical_ties:
            if self.logical_ties[0].rest:
                self.logical_ties[0].parent.pop(0)
            if self.logical_ties[-1].rest:
                self.logical_ties[-1].parent.pop(-1)