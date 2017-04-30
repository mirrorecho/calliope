import abjad
from calliope import structures

class AttachTags(object):
    """
    mixin to be used with SegmentedLine
    """
    show_data_type = None
    show_data_attr = None

    _open_spanners = None # to be set to a dict containing spanner start as they key, and music leaf index as the value

    def __init__(self, show_data_type=None, show_data_attr=None, **kwargs):
        
        # setting these here, because we want them set on self BEFORE calling super().__init__
        self.show_data_type = show_data_type or self.show_data_type
        self.show_data_attr = show_data_attr or self.show_data_attr
        self._open_spanners = {}
        super().__init__(**kwargs)

    def tag_events(self, tag=None, start_index=None, stop_index=None, every_child=False):
        for e in self.events[start_index:stop_index]:
            if every_child:
                for l in e.children:
                    l.tag(tag)
            else:
                e.tag(tag)

    # TO DO... rethink how this is implemented once bubbles are module based (better something for output settings.... )
    def show_data(self, show_data_type=None, show_data_attr=None):
        if show_data_type or show_data_attr:
            show_data_type = show_data_type or machines.EventData
            show_data_attr = show_data_attr or "depthwise_index"
            # TO DO: there must be a way to make this more elegant:
            for node in [node for node in self.data.nodes if isinstance(node, show_data_type)]:
                node.tag("data:" + show_data_attr)
        return self

    def update_data(self, **kwargs):
        super().update_data(**kwargs)
        self.show_data(self.show_data_type, self.show_data_attr)

    # TO DO... implement if useful?
    # def tag(self, *kwargs):
    #     for kwarg in kwargs:
    #         if isinstance(kwarg, dict) or isinstance(kwarg):
    #             self.attachments.update(kwarg):

    # TO DO... maybe this method should be a part of the base SegmentedLine, and only deal with the actual attachments here
    def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_index, **kwargs):
        super().process_logical_tie(music, music_logical_tie, data_logical_tie, music_leaf_index, **kwargs)
        # attachments = data_logical_tie.get_all_attachments()

        # loop through attachments to close open spanners
        for attachment_name in data_logical_tie.get_all_attachment_names():
            spanners_to_close = set(self._open_spanners) & structures.TagSet.spanner_closures.get(attachment_name, set() )
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
        for attachment_name in data_logical_tie.get_all_attachment_names():            
            if attachment_name in structures.TagSet.start_spanners_inventory:
                self._open_spanners[attachment_name]=music_leaf_index
            else:
                attachment = data_logical_tie.get_attachment(attachment_name)
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
            # print(attachment_name)
        # print("-------------------------------------------------")
            
    def process_logical_ties(self, music, **kwargs):
        self._open_spanners = {} # important in case music() metchod gets called twice on the same object
        super().process_logical_ties(music, **kwargs)
