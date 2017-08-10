import abjad
from calliope import structures, bubbles

class TagSet(object):
    tags = None # to be set to a set
    
    # TO DO... abjad may already define these somewhere.. research:
    # TO DO... implement beaming here... would be especially userful with span_every
    articulations_inventory = set((".", "-", ">",".","^"))
    dynamics_inventory = set(("ppp","pp","p","mp","mf","f","ff","fff"))
    
    slurs_inventory = set(("(", "((")) # note... double parens could be used to indicate larger phrasing slur
    hairpins_inventory = set( ("\<","\>") ) # note... may not be needed

    start_spanners_inventory = set(("~","8va")) | slurs_inventory | hairpins_inventory
    stop_spanners_inventory = set( (")", "))", "\!", "~!","8va!"), )
    stem_tremolos_inventory = set( (":8",":16",":32") )
    tremolos_inventory = set( ("tremolo:1", "tremolo:2", "tremolo:3",) )
    colors_inventory = set(("red",         "green",
                "blue",        "cyan",           "magenta",     "yellow",
                "grey",        "darkred",        "darkgreen",   "darkblue",
                "darkcyan",    "darkmagenta",    "darkyellow",))

    # TO DO... should prevent dupes in tremolos

    # defines things that the spanners close:
    spanner_closures = {
        "8va!": set(("8va",)), # (made up shorthand for end octavation)
        ")":    set(("(",)),
        "))":   set(("((",)),
        "~!":   set(("~",)), # (made up shorthand for end tie)
    }
    for item in dynamics_inventory | hairpins_inventory | set( ("\!",) ):
        spanner_closures[item] = hairpins_inventory

    def __init__(self, *args, **kwargs):
        self.tags = set()
        super().__init__(*args, **kwargs)

    def get_attachment(self, tag_name):
        if tag_name in self.articulations_inventory:
            return abjad.Articulation(name=tag_name)
        elif tag_name in self.dynamics_inventory:
            return abjad.Dynamic(name=tag_name)
        elif tag_name in self.slurs_inventory:
            return abjad.Slur()
        elif tag_name == "\<":
            return abjad.Crescendo()
        elif tag_name == "\>":
            return abjad.Decrescendo()
        elif tag_name in self.stem_tremolos_inventory:
            tremolo_flags = int(tag_name[1:])
            return abjad.indicatortools.StemTremolo(tremolo_flags)
        elif tag_name in self.tremolos_inventory:
            tremolo_count = int(tag_name[8:])
            return abjad.indicatortools.Tremolo(beam_count=tremolo_count, is_slurred=True)
        elif tag_name == "~":
            return abjad.spannertools.Tie()
        elif tag_name == "8va":
            return abjad.spannertools.OctavationSpanner(start=1)
        elif tag_name in self.colors_inventory:
            # return lambda x : abjad.agenttools.LabelAgent(x).color_leaves(tag_name)
            pass
        elif not tag_name in self.stop_spanners_inventory:
            if tag_name[0] == "\\":
                return abjad.indicatortools.LilyPondCommand(tag_name[1:])
            else:
                return abjad.Markup(tag_name, direction=Up)

    # TO DO... only if needed
    # def get_attachments(self, **kwargs):
    #     return [AttachmentSetData.get_attachment(a) for a in self.tags]

    def set_tag(self, my_set, *args):
        for arg in args:
            if arg[:5] == "data:":
                my_set.add(str(getattr(self, arg[5:])))
            else:
                # ovewrite existing dynamics and hairpins:
                if arg in self.dynamics_inventory:
                    my_set -= self.dynamics_inventory
                elif arg in self.hairpins_inventory:
                    my_set -= self.hairpins_inventory
                my_set.add(arg)        

    def tag(self, *args):
        self.set_tag(self.tags, *args)
        return self

    # TO DO... too confusing? REMOVE?
    def tag_children(self, *args):
        for arg in args:
            if isinstance(arg, stuctures.Series):
                for i, child in enumerate(self.children):
                    child_set = set(arg[i])
                    # ovewrite existing dynamics and hairpins:
                    if child_set & self.dynamics_inventory:
                        child.tags -= self.dynamics_inventory
                    if child_set & self.hairpins_inventory:
                        child.tags -= self.hairpins_inventory
                    child.tags |= child_set
            else:
                for child in self.children:
                    child.tag(arg)
        return self

    def untag(self, *args):
        for arg in args:
            if arg in self.tags:
                self.tags.remove(arg)
        return self

	# TO DO... too confusing? REMOVE?
    def untag_children(self, *args):
        for arg in args:
            if isinstance(arg, stuctures.Series):
                for i, child in enumerate(self.children):
                    child.tags -= set(arg[i])
            else:
                for child in self.children:
                    child.tags.remove(arg)
        return self

    def combine_tags(self, new_set, old_set):
        # note, can't do simple union since that could dupe dynamics or hairpins, so need to call set_tag method on each one
        # .... here, new_set values override old_set values for hairpins and dynamics
        combined_set = set(old_set) # makes a copy
        for n in new_set:
            self.set_tag(combined_set, n)
        return combined_set

    # TO DO add if useful...
    # def tag_children(self, *args):
    #     for arg in args:
    #         self.tags.add(arg)

    @property
    def use_ancestor_attachments(self): 
        """
        in general, the first item uses parent attachments (e.g. if event is first item in a segment, and a segment
        is tagged with "mf", then event is event is also "mf"... but not if event is second item in the segment)
        ...overriden in LogicalTieData so that the first NONREST item uses ancestor attachments (instead of first item)
        """
        return self.my_index == 0 

    def get_ancestor_tags(self):
        if self.parent and self.use_ancestor_attachments and hasattr(self.parent, "tags"):
            return self.combine_tags(self.parent.tags, self.parent.get_ancestor_tags())
        else:
            return set()

    def get_all_tags(self):
        return self.combine_tags(self.tags, self.get_ancestor_tags())

    # TO DO... consider implementing this
    # # TO DO.. this should be able to work with original_depthwise_index (or fragments should not reset segments)
    # def span_children(self, spanner):
    #     # TO DO... something more elegant to associate spanners with end spanners
    #     if spanner == "(":
    #         end_spanner = ")"
    #     if spanner == "((":
    #         end_spanner = "))"
    #     if spanner == "\<" or spanner == "\>":
    #         end_spanner = "\!"
    #     self.children[0]

    # TO DO... remove in favor of always using Transform objects?
    @classmethod
    def span_every(cls, spanner, items, every_count=2):
        # TO DO... something more elegant to associate spanners with end spanners
        if spanner == "(":
            end_spanner = ")"
        if spanner == "((":
            end_spanner = "))"
        if spanner == "\<" or spanner == "\>":
            end_spanner = "\!"
        
        for i in range(0, len(items), every_count):
            items[i].tag(spanner)
            if len(items) > i+every_count-1:
                items[i+every_count-1].tag(end_spanner)

    # TO DO.. only if needed:
    # def get_all_attachments(self):
    #     """
    #     Funny and slightly confusing method... 
    #     """
    #     return [self.get_attachment(a) for a in self.get_all_names()]

    # TO DO... implement only if needed
    # def get_descendant_names(self):
    #     if self.children:
    #         return self.children[0].tags | self.get_descendant_names()
    #     else:
    #         return set()

    # def get_consolidated_names(self):
    #     return self.tags | self.get_ancestor_names() | self.get_descendant_names()

    # def get_consolidated_attachments(self):
    #     """
    #     Funny and slightly confusing method... 
    #     """
    #     return [AttachmentSetData.get_attachment(a) for a in self.get_consolidated_names()]
